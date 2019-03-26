import asyncio, asyncssh, sys, os, time, datetime, smtplib
from email.message import EmailMessage


class Jbt:
    # Jbt means `Jenkins backup transfer`
    destination_path = '//khlopov18..local/SharedSpace/Jenkins_backup_prod/Jenkins_backup_all/'
    remote_path = '/var/tmp/Jenkins_backup_all/'
    ssh_key_file = 'C:\AlexkH\ssh_keys\jnksrv_backup_key'
    remote_host = 'jnknssrv-01'
    backup_rotation_days = 15
    destination_size = 0
    backup_transfer_results = 'not started'
    smtp_server = 'rusmtp..com'
    smtp_port = 25
    email_from = 'jenkins_backup@.com'
    email_to = 'Alexander.@.com'
    email_body = ''


async def run_client():
    """
    starts ssh-client in async mode and getting backup files via sftp method
    """
    async with asyncssh.connect(Jbt.remote_host, client_keys=Jbt.ssh_key_file) as conn:
        result = await conn.run('ls {}'.format(Jbt.remote_path), check=True)
        # result = await conn.run('ls /var/tmp/Jenkins_backup_all', check=True)
        print(result.stdout, end='')
        files_on_remote = result.stdout.split('\n')
        # print(files_on_remote)
        for f in files_on_remote:
            if (os.path.isfile(Jbt.destination_path + f)):
                print('FILE ALREADY EXISTS: ' + f)
            else:
                if (f):
                    print('NO SUCH FILE ' + f + ' - downloading')
                    try:
                        async with conn.start_sftp_client() as sftp:
                            await sftp.get(Jbt.remote_path + f, Jbt.destination_path)
                            # await sftp.get('/var/tmp/Jenkins_backup_all/' + f, Jbt.destination_path)
                            Jbt.backup_transfer_results = 'SUCCESS'
                    except Exception as e:
                        Jbt.backup_transfer_results = 'FAILED'
                        print(e)


def cleanup_old_backups(path):
    """
    cleaning the destination path, given in the argument.
    Note: if less than 4 files in the destination, cleanup will be skipped (to have at least two last backups)
    :param path: destination path, example: //your.pc.local/SharedSpace/
    """
    if (len(os.listdir(path)) > 4):
        # do cleanup in provided `path`
        current_timestamp = time.time()
        old_file_time_delta = datetime.timedelta(days=Jbt.backup_rotation_days).total_seconds()
        for backupfile in os.listdir(path):
            # created_timestamp = os.path.getctime(Jbt.destination_path + backupfile)
            modifyed_timestamp = os.path.getmtime(path + backupfile)
            if (current_timestamp - modifyed_timestamp > old_file_time_delta):
                print('old file: ' + backupfile + ' - removing')
                os.remove(path + backupfile)
    else:
        print('there are not much files for cleanup')
    get_size(Jbt.destination_path)


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
    Jbt.destination_size = round((total_size / 1024)/1024)


def send_results():
    """
    sending results to email
    """
    for files in os.listdir(Jbt.destination_path):
        Jbt.email_body += files + " <br> "
    # Create the base text message.
    destination_size = os.stat(Jbt.destination_path)
    msg = EmailMessage()
    msg['Subject'] = "Jenkins Backup {}".format(Jbt.backup_transfer_results)
    msg['From'] = Jbt.email_from
    msg['To'] = Jbt.email_to
    email_content = '<h3>List of destination directory ({} MB) :</h3> <b>{}</b> <br> {}'.format(Jbt.destination_size,
                                                                                        Jbt.destination_path,
                                                                                        Jbt.email_body)
    msg.set_content(email_content)
    msg.set_type('text/html')
    # Send the message via local SMTP server.
    with smtplib.SMTP(Jbt.smtp_server, port=Jbt.smtp_port) as s:
        s.send_message(msg)


# to do:
# skip files already exits in destination folder
# cleanup destination folder from files are not exists on the remote (or just outdated)
# send email
# write issue about scp without key file!
# upload on git both scripts, PS and PY

def main():
    try:
        asyncio.get_event_loop().run_until_complete(run_client())
    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
    try:
        cleanup_old_backups(Jbt.destination_path)
    except Exception as e:
        print(e)
    send_results()


if __name__ == "__main__":
    main()
