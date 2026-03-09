#!/usr/bin/python

import logging
import configparser

from core.morse import Morse
from core.phonetic import Phonetic


class Identification:
    def __init__(self, voicesynthesizer):
        self.modulename = 'Identification'
        self.voicesynthesizer = voicesynthesizer
        self.phonetic = Phonetic()
        self.morse = Morse()

        conf = configparser.ConfigParser()
        conf.read("configuration/general.config")
        general = conf["general"]
        self.callsign = general.get("callsign")
        radioclub = general.get("radioclub")
        phonetic_callsign = ' '.join(self.phonetic.decode(self.callsign))
        self.message = f"{radioclub}, {phonetic_callsign}"

    def identify(self):
        logging.info('Identification Identify')
        self.morse.generate(f'cq cq {self.callsign}')
        self.voicesynthesizer.speech_it(self.message)
