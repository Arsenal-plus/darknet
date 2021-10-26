import json
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_image(image_path, smtp_server, smtp_port, login, password, sender_mail, recv_mail):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Object detected!'
    msgRoot['From'] = sender_mail
    msgRoot['To'] = recv_mail
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    msgText = MIMEText('<img src="cid:image1">', 'html')
    msgAlternative.attach(msgText)

    with open(image_path, 'rb') as fp:
        msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP_SSL(host=smtp_server, port=smtp_port)
    smtp.ehlo()
    smtp.login(login, password)
    smtp.sendmail(sender_mail, recv_mail, msgRoot.as_string())
    smtp.close()


if __name__ == "__main__":
    with open('darknet_scripts.json') as json_file:
        config = json.load(json_file)
    send_image(sys.argv[1], config['smtp_server'], config['smtp_port'],
               config['user_login'], config['user_password'],
               config['sender_mail'], config['recv_mail'])
