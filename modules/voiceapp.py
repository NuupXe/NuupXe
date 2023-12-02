#!/usr/bin/python

import subprocess
import logging
import json
import time

from core.alive import alive
from core.voiceapplication import VoiceApplication
from core.voicesynthetizer import VoiceSynthetizer
from pprint import pprint

class VoiceApp(object):

    def __init__(self, voicesynthetizer):
        self.modulename = 'Voice Application'
        self.voicesynthetizer = voicesynthetizer
        self.voiceapplication = VoiceApplication()

    def application(self):
        logging.info(self.modulename)
        repeater = 'python nuupxe.py -v \"Hola! En que puedo ayudarte?\"'
        status, output = commands.getstatusoutput(repeater)
        response = self.voiceapplication.action()
        repeater = 'python nuupxe.py -m \"' + response + '\"'
        status, output = commands.getstatusoutput(repeater)

# End of File
