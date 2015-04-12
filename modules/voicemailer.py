#!/usr/bin/python

import ConfigParser
import commands
import logging

from core.emailx import Emailx
from core.irlp import Irlp
from core.phonetic import Phonetic
from core.pushtotalk import PushToTalk
from core.voice import Voice
from core.voicerecognition import VoiceRecognition

class VoiceMailer(object):

    def __init__(self, voicesynthetizer):

        self.emailx = Emailx()
        self.irlp = Irlp()
        self.phonetic = Phonetic()
        self.pushtotalk = PushToTalk()
        self.voice = Voice()
        self.voicerecognition = VoiceRecognition(voicesynthetizer)

        self.conf = ConfigParser.ConfigParser()
        self.filepath = "configuration/voicemailer.config"
        self.conf.read(self.filepath)

        self.voicesynthetizer = voicesynthetizer

    def __del__(self):
        pass

    def decodeUser(self, dmtf):
        logging.info('Voice Mailer Decode User')
        user = dmtf[2:]
        try:
            callsign = self.conf.get(user, "callsign")
            email = self.conf.get(user, "email")
        except ConfigParser.NoSectionError:
            return None, None
        return callsign, email

    def attend(self, dtmf):

        logging.info('Voice Mailer Attend')

        user, email = self.decodeUser(dtmf)
        if user:
            user = ' '.join(self.phonetic.decode(user))
            self.voicesynthetizer.speechit("Mensaje para " + user)
            self.voicesynthetizer.speechit('Cual es tu mensaje?')
            self.voicerecognition.record()
            message = self.voicerecognition.recognize('False')
            logging.info('Mensaje? ' + message)
            self.voicesynthetizer.speechit(message)
            filename = self.voicerecognition.filegetname()
            self.emailx.create(email, 'NuupXe Voice Mailer! Mensaje ...', message, filename)
            self.emailx.send()
        else:
            self.voicesynthetizer.speechit('Usuario no asignado!')

# Enf of File

