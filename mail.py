from email.mime.text import MIMEText
from email.header import Header
import smtplib, ssl


class Mailer(object):
    def __init__(self, user, password, host='smtp.yandex.ru', timeout=5):
        self.user = user
        self.password = password
        self.host = host
        self.timeout = timeout
        self.connected = False
        self.smtp = None

    def connect(self):
        if not self.connected:
            mail_context = ssl.create_default_context()
            self.smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465, timeout=self.timeout, context=mail_context)
            self.smtp.login(self.user, self.password)
            self.connected = True

    def send_email(self, from_, to, subject, content):
        if to is None:
            return False

        self.connect()
        if not isinstance(to, list):
            to = [to]

        msg = MIMEText(content, 'html', _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = from_
        msg['To'] = ','.join(to)

        self.smtp.sendmail(from_, to, str(msg))

    def close(self):
        self.smtp.close()
