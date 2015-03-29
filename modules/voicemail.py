#!/usr/bin/python

import commands
import time

from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.voice import Voice

class VoiceMail(object):

    def __init__(self, voicesynthetizer):

        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.voice = Voice()

        self.voicesynthetizer = voicesynthetizer
        self.audiofileuser = 'output/voicemailuser'
        self.audiofilemessage = 'output/voicemailmessage'

    def __del__(self):
        pass

    def record(self):
        print '[Cancun] Voice Mail Record'
        self.voice.record()

    def play(self):
        print '[Cancun] Voice Mail Play'
        self.voice.play()

    def run(self, dtmf):
        print '[Cancun] Voice Mail Run'

	if dtmf:
            self.voicesynthetizer.speechit("Codigo recibido " + dtmf)
        self.voicesynthetizer.speechit("Identificate por favor")
        self.voice.filenameset(self.audiofileuser)
        self.record()

        self.voicesynthetizer.speechit("Deja tu mensaje")
        self.voice.filenameset(self.audiofilemessage)
        self.record()

        self.voicesynthetizer.speechit("Mensaje de")
        self.voice.filenameset(self.audiofileuser)
        self.play()
        self.voice.filenameset(self.audiofilemessage)
        self.play()

# Enf of File

