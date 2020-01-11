import configparser
import smtplib as smtp

config = configparser.ConfigParser()
config.read('config.ini')


def send_email(subject, message, dest):
    email = config.get('mail', 'email')
    password = config.get('mail', 'password')

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                           dest,
                                                           subject,
                                                           message)

    server = smtp.SMTP_SSL(config.get('mail', 'server'))
    server.ehlo(email)
    server.login(email, password)
    server.auth_plain()
    server.sendmail(email, dest, message)
    server.quit()
