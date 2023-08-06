import os
import smtplib
from email.mime.text import MIMEText

from passlib.hash import pbkdf2_sha256


class Helper:

    @staticmethod
    def verify_crypt(password, compare_password):
        print("pass", password, compare_password)
        return pbkdf2_sha256.verify(password, compare_password)

    @staticmethod
    def set_crypt(password):
        print("que pex", password)
        return pbkdf2_sha256.hash(password)


    @staticmethod
    def send_mail(to, subject, content):
        mail_user = os.environ.get('MAIL_USER', "")
        mail_pass = os.environ.get('MAIL_PASS', "")
        smtpserver = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(mail_user, mail_pass)
        from_email = 'edominguez@auriz.biz'
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to
        smtpserver.sendmail(from_email, [to], msg.as_string())
        smtpserver.quit()
