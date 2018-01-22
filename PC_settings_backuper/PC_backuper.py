import backup_cfg
import zipfile
import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def backupme():
    backupinstance = backup_cfg.PC_backup()
    zipinstance = zipfile.ZipFile
    try:
        os.remove(backupinstance.backup_to)
    except:
        pass
    try:
        for backupfolder in backupinstance.backup_from:
            for entry in os.scandir(backupfolder):
                print(entry.path)
                zipinstance(backupinstance.backup_to, "a").write(entry.path)
    except Exception as error:
        print(error)

    try:
        msg = MIMEMultipart()
        msg['Subject'] = backupinstance.mail_subject
        msg['From'] = backupinstance.send_backup_to
        msg['To'] = backupinstance.send_backup_to
        with open(backupinstance.backup_to, 'rb') as fp:
            msg_file = MIMEBase('application', "octet-stream")
            msg_file.set_payload(fp.read())
        encoders.encode_base64(msg_file)
        msg_file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(backupinstance.backup_to))
        msg.attach(msg_file)

        # Send the email:
        with smtplib.SMTP(backupinstance.mail_server) as s:
            s.send_message(msg)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    backupme()