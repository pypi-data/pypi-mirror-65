from passlib.hash import pbkdf2_sha256
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Helper:

    @staticmethod
    def verify_crypt(password, compare_password):
        return pbkdf2_sha256.verify(password, compare_password)

    @staticmethod
    def set_crypt(password):
        return pbkdf2_sha256.hash(password)


    @staticmethod
    def send_mail(to, subject, content):
        message = Mail(
            from_email='no-reply@groundworx.com',
            to_emails=to,
            subject=subject,
            html_content=content
        )
        try:
            sg = SendGridAPIClient("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")
            sg.send(message)
        except Exception as e:
            pass
