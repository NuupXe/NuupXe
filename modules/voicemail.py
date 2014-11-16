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

	self.status = False
        self.audiofilewav = "voicemail.wav"
        self.voicesynthetizer = voicesynthetizer

    def __del__(self):
        pass
        #status, output = commands.getstatusoutput("rm " + self.audiofilewav)

    def status(self):
	return self.status

    def record(self):
        print '[Cancun] Voice Mail Record'
	self.voicesynthetizer.speechit("Graba el mensaje")
        time.sleep(1)
        while self.irlp.cosenabled() is 256:
            pass
        while self.irlp.cosenabled() is 0:
            pass
        proc = self.voice.recordstart()
        while self.irlp.cosenabled() is 256:
            pass
        self.voice.recordstop(proc)

    def play(self):
        print '[Cancun] Voice Mail Play'
        self.pushtotalk.openport()
        self.voice.play()
        self.pushtotalk.closeport()

    def erase(self):
        print '[Cancun] Voice Mail Erase'
	self.voicesynthetizer.speechit("Borrando el mensaje")
        self.voice.erase()

    def run(self):
        print '[Cancun] Voice Mail Run'
        self.record()
        self.play()
        self.erase()

if __name__ == '__main__':

    mytest = VoiceMail()
    mytest.record()
    mytest.play()

