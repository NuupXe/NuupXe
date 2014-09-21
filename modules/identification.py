#!/usr/bin/python

import ConfigParser

from core.morse import Morse
from core.phonetic import Phonetic
from core.voicesynthetizer import VoiceSynthetizer

class Identification(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.morse = Morse()
        self.voicesynthetizer = voicesynthetizer
        
        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

    def identify(self):
        print '[Cancun] Identification'
        self.morse.generate('cq')
        self.voicesynthetizer.speechit(self.conf.get("general", "radioclub"))
        self.voicesynthetizer.speechit(self.conf.get("general", "systemname"))
        message = " operado por " + ' '.join(self.phonetic.decode(self.conf.get("general", "callsign")))
        message = "\"" + message + "\""
        self.voicesynthetizer.speechit(message)
        self.morse.generate(self.conf.get("general", "callsign"))

if __name__ == '__main__':

    mytest = Identification()
    mytest.identify()
