#!/usr/bin/python

import commands

from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

class VoiceCommand(object):

    def __init__(self, voicesynthetizer):

	self.output = ""
        self.agent = "google"
        self.audiofilewav = "audio.wav"
        self.audiofilewavcompand = "audioc.wav"
        self.audiofilewavnoise = "audion.wav"
        self.audiofileflac = "audio.flac"
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()
        self.voicetospeech = VoiceToSpeech()

    def __del__(self):

        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
        status, output = commands.getstatusoutput("rm " + self.audiofileflac)

    def record(self, seconds):

        print '[Cancun] Voice Command Record'

        if self.agent == 'nexiwave':
                status, output = commands.getstatusoutput("arecord -vv -f cd -d " + seconds + " " + self.audiofile)
        elif self.agent == 'google':
                status, output = commands.getstatusoutput("arecord -d " + seconds + " -f dat -t wav -r 48000 -c 2 " + self.audiofilewav)
                status, output = commands.getstatusoutput("sox " + self.audiofilewav + " " + self.audiofilewavcompand + " compand 0.02,0.20 5:-60,-40,-10 -5 -90 0.1")
                status, output = commands.getstatusoutput("sox " + self.audiofilewav + " -n remix 1 trim 0 1 noiseprof noise.prof")
                status, output = commands.getstatusoutput("sox " + self.audiofilewav + " " + self.audiofilewavnoise + " remix 1 noisered noise.prof")
                status, output = commands.getstatusoutput("flac -f -o " + self.audiofileflac + " --channels=1 --sample-rate=48000 " + self.audiofilewavnoise)

    def decode(self, speech):

        print '[Cancun] Voice Command Decode'

	if speech == 'True':
                self.voicesynthetizer.speechit("Estamos procesando tu respuesta")
                self.pushtotalk.openport()
                status, output = commands.getstatusoutput("aplay " + self.audiofilewav)
                status, output = commands.getstatusoutput("aplay " + self.audiofilewavcompand)
                status, output = commands.getstatusoutput("aplay " + self.audiofilewavnoise)
                self.pushtotalk.closeport()

        status, output = commands.getstatusoutput("aplay " + self.audiofilewavnoise)
        print output

        if self.agent == 'nexiwave':
                self.voicetospeech.nexiwave(self.audiofile)
        elif self.agent == 'google':
                self.output = self.voicetospeech.google(self.audiofileflac)
                print self.output

        return self.output

if __name__ == '__main__':

    mytest = Command()
    mytest.record()
    mytest.play()
