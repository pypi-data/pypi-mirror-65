from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from smtplib import SMTP_SSL
from jinja2 import Environment, FileSystemLoader
import os
from Core.Log import Log


class EmailHelper:
    def __init__(self, **kwargs):
        self.host_server = kwargs.get('host_server', os.getenv('EMAIL_HOST_SERVER', ''))
        self.sender = kwargs.get('sender', os.getenv('EMAIL_SENDER', ''))
        self.password = kwargs.get('password', os.getenv('EMAIL_PASSWORD', ''))
        self.log = kwargs.get('log', Log(self.__class__.__name__))

    def send_email(self, receiver,  **kwargs):
        mail_content = self.get_mail_content()
        receiver = self.get_receivers(receiver)
        try:
            mail_title = 'QA3:'
            msg = MIMEMultipart()
            msg['Subject'] = Header(mail_title, 'utf-8')
            msg['From'] = self.sender
            context = MIMEText(mail_content, _subtype='html', _charset='utf-8')
            msg.attach(context)

            smtp = SMTP_SSL(self.host_server)
            smtp.set_debuglevel(0)
            smtp.ehlo(self.host_server)
            smtp.login(self.sender, self.password)
            msg["To"] = receiver
            smtp.sendmail(self.sender, receiver, msg.as_string())
            smtp.quit()
        except Exception as e:
            self.log.error('failed to send email %s' % str(e))

    def get_receivers(self, receiver_input):
        receiver = 'will.wei@72degreedata.cn,577452271@qq.com'
        pass

    def get_mail_content(self, content_input):

        pass


class QaEmailHelper(EmailHelper):
    def __init(self, **kwargs):
        super(QaEmailHelper, self).__init__(**kwargs)


if __name__ == '__main__':
    t = EmailHelper()
    t.send_email()
