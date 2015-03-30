#!/usr/bin/python

import ConfigParser
import smtplib
import email

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class Emailx(object):

    def __init__(self):
        self.me = 'arjac.cancun@gmail.com'
        self.to = 'arjac.cancun@gmail.com'
        self.body = 'Default Body'
        self.subject = 'Default Subject'
        self.msg = MIMEMultipart('alternative')
        self.msg.set_charset('utf8')

        self.setup()
        self.create(self.to, self.subject, self.body)

    def setup(self):

        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/services.config')
        self.username = self.configuration.get('gmail','username')
        self.password = self.configuration.get('gmail','password')

    def create(self, to, subject, body, attachment=None):

        self.msg = MIMEMultipart()
        self.msg['Subject'] = subject
        self.msg['From'] = self.me
        self.msg['To'] = to
        self.msg.attach(MIMEText(body.encode('utf-8'), 'html', 'UTF-8'))

        if attachment:
            file = open(attachment, "rb")
            self.msg.attach(MIMEApplication(
                file.read(),
                Content_Disposition='attachment; filename="%s"' % basename(attachment)
            ))

    def send(self):

        server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        server.login(self.username, self.password)
        server.sendmail(self.me, [self.to], self.msg.as_string())
        server.quit()

# End of File
