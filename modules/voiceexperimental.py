#!/usr/bin/python

import json
import logging

from core.emailx import Emailx
from core.twitterc import TwitterC
from core.voicerecognition import VoiceRecognition

class VoiceExperimental(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.emailx = Emailx()
        self.twitterc = TwitterC('twython')
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)

        self.setup()

    def __del__(self):

        self.cleanup()

    def setup(self):

        logging.info('Voice Experimental Setup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def cleanup(self):

        logging.info('Voice Experimental Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def listen(self):

        logging.info('Voice Experimental Listen')
        self.voicesynthetizer.speechit('Hola! Dime tu frase!')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        logging.info('Phrase? ' + question)
        self.voicesynthetizer.speechit(question)
        question = '#HamRadio #ProyectoCancun #VoiceExperimental ... ' + question.capitalize()
        self.twitterc.timeline_set(question, media=None)
        self.emailx.create('arjac.cacun', 'Voice Experimental Listen', question)
        self.emailx.send()

# End of File
