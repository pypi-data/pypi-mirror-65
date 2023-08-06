from passlib.hash import pbkdf2_sha256
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
        message = Mail(
            from_email='no-reply@groundworx.com',
            to_emails=to,
            subject=subject,
            html_content=content
        )
        try:
            sg = SendGridAPIClient("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")
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("error", e)
            pass
