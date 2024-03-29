#!/usr/bin/python

import configparser
import smtplib
import email

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class Emailx(object):

    def __init__(self):
        self.me = None
        self.to = None
        self.body = 'Default Body'
        self.subject = 'Default Subject'
        self.msg = MIMEMultipart('alternative')
        self.msg.set_charset('utf8')

    def setup(self):

        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/services.config')
        self.username = self.configuration.get('gmail','username')
        self.password = self.configuration.get('gmail','password')

        self.system = ConfigParser.ConfigParser()
        self.system.read('configuration/general.config')
        self.me = self.system.get('system','email')
        self.to = self.me

    def create(self, to, subject, body, attachment=None):

        self.setup()
        self.to = to

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
