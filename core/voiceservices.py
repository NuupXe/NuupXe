#!/usr/bin/python

import commands

from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

class VoiceServices(object):

    def __init__(self, voicesynthetizer):
	self.status = False
	self.output = ""
        self.audiofilewav = "voiceservices.wav"
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()
        self.voicetospeech = VoiceToSpeech()

    def __del__(self):
        status, output = commands.getstatusoutput("rm " + self.audiofilewav)

    def status(self):
	return self.status

    def record(self, seconds):
        print '[Cancun] Voice Services Record'
	self.voicesynthetizer.speechit("Graba tu mensaje en los proximos " + seconds + " segundos")
        status, output = commands.getstatusoutput("arecord -d " + seconds + " -f dat -t wav -r 48000 -c 2 " + self.audiofilewav)
	self.status = True

    def erase(self):
        print '[Cancun] Voice Services Erase'
	self.voicesynthetizer.speechit("Borrando mensaje")
        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
	self.status = False

    def play(self):
        print '[Cancun] Voice Services Play'
        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofilewav)
        self.pushtotalk.closeport()

if __name__ == '__main__':

    mytest = VoiceServices()
    mytest.record()
    mytest.play()

