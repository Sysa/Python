import os, time, datetime, smtplib, shutil, argparse
from email.message import EmailMessage


class Clnp:
    destination_path = '//khlopov18.localhost.local/SharedSpace/cleanup_files_check/'
    backup_rotation_days = 0
    destination_size = 0
    number_of_files_or_folders_to_keep = 4
    email_subject_result = 'not started'
    smtp_server = 'rusmtp.localhost.com'
    smtp_port = 25
    email_from = 'jenkins_cleanup@localhost.com'
    email_to = 'Alexander.Khlopov@localhost.com'
    email_body = ''
    email_job_url = ''


def cleanup_old_files(path):
    """
    cleaning the destination path, given in the argument.
    Note: if less than 4 files in the destination, cleanup will be skipped (to have at least two last backups)
    Note: it is checking only directories without subfolders!
    :param path: destination path, example: //your.pc.local/SharedSpace/
    """
    if (len(os.listdir(path)) > Clnp.number_of_files_or_folders_to_keep):
        # do cleanup in provided `path`
        current_timestamp = time.time()
        old_file_time_delta = datetime.timedelta(days=Clnp.backup_rotation_days).total_seconds()

        list_dir_result = []
        for backupfile in os.listdir(path):
            list_dir_result.append(path + backupfile)  # = path + backupfile
        # print(list_dir_result)
        list_dir_result.sort(key=sort_by_modify_time)
        # print(list_dir_result)

        # for backupfile in os.listdir(path):
        for backupfile in list_dir_result:
            # created_timestamp = os.path.getctime(Clnp.destination_path + backupfile)
            # modifyed_timestamp = os.path.getmtime(path + backupfile)
            modifyed_timestamp = os.path.getmtime(backupfile)
            # print(backupfile + " ->>>>> " + str(modifyed_timestamp))
            if (current_timestamp - modifyed_timestamp > old_file_time_delta):
                # while len(os.listdir(path)) > Clnp.number_of_files_or_folders_to_keep:
                if (len(os.listdir(path)) > Clnp.number_of_files_or_folders_to_keep):
                    print('old file: ' + backupfile + ' - removing')
                    # if(os.path.isdir(path + backupfile)):
                    if (os.path.isdir(backupfile)):
                        try:
                            # os.rmdir(path + backupfile)
                            os.rmdir(backupfile)
                        except OSError as e:
                            # print(e)  # folder not empty
                            # shutil.rmtree(path + backupfile)
                            shutil.rmtree(backupfile)
                    else:
                        # os.remove(path + backupfile)
                        os.remove(backupfile)
                    Clnp.email_subject_result = "completed"
    else:
        print('There are not much files for cleanup')
        Clnp.email_subject_result = "- there are not much files for cleanup"
    get_size(Clnp.destination_path)


def sort_by_modify_time(path):
    try:
        modify_timestamp = os.path.getmtime(path)
        return modify_timestamp
    except Exception as e:
        print(e)


def get_size(path):
    """
    calculating size of destination path, including subfolders
    :param path: destination path, example: //your.pc.local/SharedSpace/
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    Clnp.destination_size = round((total_size / 1024) / 1024)


def send_results():
    """
    sending results to email
    """
    for files in os.listdir(Clnp.destination_path):
        Clnp.email_body += files + " <br> "
    Clnp.email_body += "<br>" + "<a href =" + Clnp.email_job_url + "> Project page in Jenkins </a>"
    # Create the base text message.
    # destination_size = os.stat(Clnp.destination_path)
    msg = EmailMessage()
    msg['Subject'] = "Jenkins Cleanup {}".format(Clnp.email_subject_result)
    msg['From'] = Clnp.email_from
    msg['To'] = Clnp.email_to
    email_content = '<h3>List of destination directory ({} MB) :</h3> <b>{}</b> <br> {}'.format(Clnp.destination_size,
                                                                                                Clnp.destination_path,
                                                                                                Clnp.email_body)
    msg.set_content(email_content)
    msg.set_type('text/html')
    # Send the message via local SMTP server.
    with smtplib.SMTP(Clnp.smtp_server, port=Clnp.smtp_port) as s:
        s.send_message(msg)


def main():
    try:
        argparser = argparse.ArgumentParser()
        argparser.add_argument("--path",
                               type=str,
                               help="path for cleanup, for example "
                                    "//C:/Users/Alex/Downloads/")
        argparser.add_argument("--ttl", type=int, help="Time To Live - count of days since today, "
                                                       "files older than this counter will be removed")
        argparser.add_argument("--kl", type=int, help="Keep Last - N number of files, "
                                                      "which must be alive after cleanup. "
                                                      "Only N newest files will be in safe")
        argparser.add_argument("--emails", type=str, help="E-mails to which execution report should to go."
                                                          "Emails separates by comma `,` and passes in one string."
                                                          "Example: a@a.com,b@b.ru,etc@etc.net")
        argparser.add_argument("--job_url", type=str, help="Optional, generally set by Jenkins environment variable.")
        arguments = argparser.parse_args()
        # print(arguments)
        if arguments.kl:
            Clnp.number_of_files_or_folders_to_keep = arguments.kl
        if arguments.ttl:
            Clnp.backup_rotation_days = arguments.ttl
        if arguments.emails:
            # print(arguments.emails)
            Clnp.email_to = arguments.emails
        if arguments.job_url:
            Clnp.email_job_url = arguments.job_url
        if arguments.path:
            Clnp.destination_path = arguments.path
            # print(arguments.path)
            try:
                cleanup_old_files(arguments.path)
            except Exception as exc:
                print(exc)
            send_results()
        else:
            try:
                print("No valid parameters given, default path value will be used")
                cleanup_old_files(Clnp.destination_path)
            except Exception as exc:
                print(exc)
            send_results()
    except Exception as e:
        print("No valid parameters given")
        print(e)


if __name__ == "__main__":
    main()
