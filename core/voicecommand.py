#!/usr/bin/python

import commands

from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

class VoiceCommand(object):

    def __init__(self, voicesynthetizer):

	self.output = ""
        self.agent = "google"
        self.audiofilewav = "audio.wav"
        self.audiofileflac = "audio.flac"
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()
        self.voicetospeech = VoiceToSpeech()

    def __del__(self):

        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
        status, output = commands.getstatusoutput("rm " + self.audiofileflac)

    def record(self):

        print '[Cancun] Voice Command Record'

        if self.agent == 'nexiwave':
                status, output = commands.getstatusoutput("arecord -vv -f cd -d 5 " + self.audiofile)
        elif self.agent == 'google':
                status, output = commands.getstatusoutput("arecord -d 6 -f dat -t wav -r 48000 -c 2 " + self.audiofilewav)
                status, output = commands.getstatusoutput("flac -f -o " + self.audiofileflac + " --channels=2 --sample-rate=44100 " + self.audiofilewav)

    def decode(self):

        print '[Cancun] Voice Command Decode'

	self.voicesynthetizer.speechit("Estamos procesando tu respuesta")

        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofilewav)
        self.pushtotalk.closeport()
        
        if self.agent == 'nexiwave':
                self.voicetospeech.nexiwave(self.audiofile)
        elif self.agent == 'google':
                self.output = self.voicetospeech.google(self.audiofileflac)

        return self.output

if __name__ == '__main__':

    mytest = Command()
    mytest.record()
    mytest.play()
