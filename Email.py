import smtplib
from app import db


class Email:
    def __init__(self, email_username):
        acc = CompanyEmail.query.filter_by(username=email_username).first()
        self.email = '{}@gmail.com'.format(acc.username)
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.login(acc.username, acc.password)

    def welcome_email(self, username: str, user_email: str):
        subject = 'Welcome to VideoVault'
        text = 'Welcome {} to Videovault.\n' \
               'You have 30 days before your VideoVault subscription expires.'.format(username)
        message = 'Subject: {}\n\n{}'.format(subject, text)

        self.server.sendmail(self.email, user_email, message)
        self.server.quit()
        return 'Email Sent'


class CompanyEmail(db.Model):
    __tablename__ = 'CompanyEmail'

    username = db.Column(db.VARCHAR, primary_key=True)
    password = db.Column(db.VARCHAR)

    def __init__(self):
        pass
