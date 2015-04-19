#!/usr/bin/python

import commands
import time

from core.alive import alive
from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.voice import Voice

class VoiceMail(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'VoiceMail'
        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.voice = Voice()

        self.voicesynthetizer = voicesynthetizer
        self.audiofileuser = 'output/voicemailuser'
        self.audiofilemessage = 'output/voicemailmessage'

    def __del__(self):
        pass

    def record(self):
        print '[NuupXe] Voice Mail Record'
        self.voice.record()

    def play(self):
        print '[NuupXe] Voice Mail Play'
        self.pushtotalk.openport()
        self.voice.play()
        self.pushtotalk.closeport()

    def run(self, dtmf):
        print '[NuupXe] Voice Mail Run'

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

        alive(self.modulename)

# Enf of File

