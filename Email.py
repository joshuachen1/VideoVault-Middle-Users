import smtplib

from app import db


class Email:
    def __init__(self, email_username):
        self.email_username = email_username

    def welcome_email(self, username: str, user_email: str):
        acc = CompanyEmail.query.filter_by(username=self.email_username).first()
        email = '{}@gmail.com'.format(acc.username)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(acc.username, acc.password)

        subject = 'Welcome to VideoVault'
        text = 'Welcome {} to VideoVault.\n' \
               'You have 30 days before your VideoVault subscription expires.'.format(username)
        message = 'Subject: {}\n\n{}'.format(subject, text)

        server.sendmail(email, user_email, message)
        server.quit()
        return 'Email Sent'

    def sub_reminder_email(self, username: str, user_email: str):
        subject = 'Subscription Reminder'
        text = 'Hey {}, you have 2 days before your VideoVault subscription expires.\n' \
               'Remember to resubscribe to keep your shows!'.format(username)
        message = 'Subject: {}\n\n{}'.format(subject, text)

        self.server.sendmail(self.email, user_email, message)
        self.server.quit()
        return 'Email Sent'

    def movie_email(self, username: str, user_email: str, movie_title: str):
        subject = 'Movie Rented'
        text = 'Hey {}, you have rented the movie: {}, for the next 24 hours.\n' \
               'Enjoy the movie!'.format(username, movie_title)
        message = 'Subject: {}\n\n{}'.format(subject, text)

        self.server.sendmail(self.email, user_email, message)
        self.server.quit()
        return 'Email Sent'

    def movie_return_email(self, username: str, user_email: str, movie_title: str):
        subject = 'Movie Returned'
        text = 'Hey {}, it\'s been 24 hours!\n' \
               'The movie {} has been returned. \n'.format(username, movie_title)
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
