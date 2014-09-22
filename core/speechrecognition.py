#!/usr/bin/python

# Copyright 2012 Nexiwave Canada. All rights reserved.
# Nexiwave Canada PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

import sys, os, json, urllib2, urllib, time
import commands
import ConfigParser

# You will need python-requests package. It makes things much easier.
import requests

from pushtotalk import PushToTalk

class SpeechRecognition(object):

    def __init__(self):

        self.ptt = PushToTalk()
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/services.config"
        self.conf.read(self.path)

    def google(self, audiofile):
        self.key = self.conf.get("google", "api_key")
        #command = "curl -X POST --data-binary @'" + audiofile + "' --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=es-es&key=" + self.key +"'"
        command = "curl -X POST --data-binary @'" + audiofile + "' --header 'Content-Type: audio/x-flac; rate=48000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=es-es&key=" + self.key +"'"
        status, output = commands.getstatusoutput(command)
        return output

    def nexiwave(self, audiofile):
        # Change these:
        # Login details:
        USERNAME = "xe1gyq@gmail.com"
        PASSWORD = "Y868HVMAYN54ECV"
        filename = audiofile

        """Transcribe an audio file using Nexiwave"""
        url = 'https://api.nexiwave.com/SpeechIndexing/file/storage/' + USERNAME +'/recording/?authData.passwd=' + PASSWORD + '&auto-redirect=true&response=application/json'

        # To receive transcript in plain text, instead of html format, comment this line out (for SMS, for example)
        url = url + '&transcriptFormat=html'

        # Ready to send:
        sys.stderr.write("Send audio for transcript with " + url + "\n")
        r = requests.post(url, files={'mediaFileData': open(filename,'rb')})
        data = r.json()
        transcript = data['text']

        # Perform your magic here:
        print "Transcript for " + filename + "=" + transcript

if __name__ == '__main__':

    mytest = SpeechRecognition()
    mytest.google("hola")

