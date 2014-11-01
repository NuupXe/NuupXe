#!/usr/bin/python

import commands

from core.pushtotalk import PushToTalk

class VoiceMail(object):

    def __init__(self, voicesynthetizer):
	self.status = False
	self.output = ""
        self.audiofilewav = "voicemail.wav"
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def __del__(self):
        status, output = commands.getstatusoutput("rm " + self.audiofilewav)

    def status(self):
	return self.status

    def record(self, seconds):
        print '[Cancun] Voice Mail Record'
	self.voicesynthetizer.speechit("Graba tu mensaje en los proximos " + seconds + " segundos")
        status, output = commands.getstatusoutput("arecord -d " + seconds + " -f dat -t wav -r 48000 -c 2 " + self.audiofilewav)
	self.status = True

    def erase(self):
        print '[Cancun] Voice Mail Erase'
	self.voicesynthetizer.speechit("Borrando mensaje")
        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
	self.status = False

    def play(self):
        print '[Cancun] Voice Mail Play'
        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofilewav)
        self.pushtotalk.closeport()

if __name__ == '__main__':

    mytest = VoiceMail()
    mytest.record()
    mytest.play()

