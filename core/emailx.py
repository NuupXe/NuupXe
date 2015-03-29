#!/usr/bin/python

import ConfigParser
import smtplib
import email

from email.mime.text import MIMEText

class Emailx(object):

    def __init__(self):
        self.me = 'arjac.cancun@gmail.com'
        self.to = 'arjac.cancun@gmail.com'
        self.body = 'Default Body'
        self.subject = 'Default Subject'

        self.setup()
        self.create(self.to, self.subject, self.body)

    def setup(self):

        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/services.config')
        self.username = self.configuration.get('gmail','username')
        self.password = self.configuration.get('gmail','password')

    def create(self, to, subject, body):

        self.msg = MIMEText(body)
        self.msg['Subject'] = subject
        self.msg['From'] = self.me
        self.msg['To'] = to

    def send(self):

        server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        server.login(self.username, self.password)
        server.sendmail(self.me, [self.to], self.msg.as_string())
        server.quit()

# End of File
