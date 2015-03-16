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
        #status, output = commands.getstatusoutput("rm " + self.audiofilewav)

    def record(self):
        print '[Cancun] Voice Mail Record'
        time.sleep(1)
        while self.irlp.cosenabled() is 256:
            pass
        while self.irlp.cosenabled() is 0:
            pass
        proc = self.voice.record_start()
        while self.irlp.cosenabled() is 256:
            pass
        self.voice.record_stop(proc)

    def play(self):
        print '[Cancun] Voice Mail Play'
        self.pushtotalk.openport()
        self.voice.play()
        self.pushtotalk.closeport()

    def erase(self):
        print '[Cancun] Voice Mail Erase'
        self.voice.erase()

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

