#!/usr/bin/python

import subprocess
import logging

from core.alive import alive
from core.voiceapplication import VoiceApplication

class VoiceApp(object):

    def __init__(self, voicesynthesizer):
        self.modulename = 'Voice Application'
        self.voicesynthesizer = voicesynthesizer
        self.voiceapplication = VoiceApplication()

    def application(self):
        logging.info(self.modulename)
        self.voicesynthesizer.speech_it("Hola! En que puedo ayudarte?")
        response = self.voiceapplication.action()
        subprocess.run(['python', 'nuupxe.py', '-m', response])

# End of File
