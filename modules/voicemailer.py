#!/usr/bin/python

import ConfigParser
import commands
import logging

from core.alive import alive
from core.emailx import Emailx
from core.irlp import Irlp
from core.phonetic import Phonetic
from core.pushtotalk import PushToTalk
from core.voice import Voice
from core.voicerecognition import VoiceRecognition

class VoiceMailer(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'VoiceMailer'
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
            messagepresentation = "Mensaje para " + user + ', Cual es tu mensaje?'
            messagepresentationdecoded = "Mensaje para " + ' '.join(self.phonetic.decode(user)) + ', Cual es tu mensaje?'
            self.voicesynthetizer.speechit(messagepresentationdecoded)
            self.voicerecognition.record()
            message = self.voicerecognition.recognize('False')
            self.voicesynthetizer.speechit(message)
            messageanswer = 'Mensaje? ' + message
            logging.info(messageanswer)
            filename = self.voicerecognition.filegetname()
            self.emailx.create(email, 'NuupXe Voice Mailer! Mensaje ...', message, filename)
            self.emailx.send()
            modulemessage = messagepresentation + ' ' + messageanswer
            alive(modulename=self.modulename, modulemessage=modulemessage)
        else:
            self.voicesynthetizer.speechit('Usuario no asignado!')

# Enf of File

