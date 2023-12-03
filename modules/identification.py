#!/usr/bin/python

import logging
import configparser

from core.alive import alive
from core.morse import Morse
from core.phonetic import Phonetic
from core.voicesynthesizer import VoiceSynthesizer

class Identification:
    def __init__(self, voicesynthesizer):
        self.modulename = 'Identification'
        self.phonetic = Phonetic()
        self.morse = Morse()
        self.voicesynthesizer = voicesynthesizer
        self.conf = configparser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

    def setup(self):
        logging.info('Identification Setup')
        general_section = self.conf["general"]
        self.message = general_section.get("radioclub")
        callsign = general_section.get("callsign")
        self.messagex = f"{self.message} {callsign}"
        self.messagex = f'"{self.messagex}"'
        self.message = f'{self.message}, {" ".join(self.phonetic.decode(callsign))}'
        self.message = f'"{self.message}"'
        self.callsign = callsign

    def identify(self):
        logging.info('Identification Identify')
        self.setup()
        self.morse.generate(f'cq cq {self.callsign}')
        self.voicesynthesizer.speech_it(self.message)
        #alive(modulename=self.modulename, modulemessage=self.messagex)
