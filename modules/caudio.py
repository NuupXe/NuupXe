#!/usr/bin/python

import commands

from core.voicesynthetizer import VoiceSynthetizer
from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

class Caudio(object):

    def __init__(self, voicesynthetizer):

        self.audiofile = 'audio.wav'
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()
        self.voicetospeech = VoiceToSpeech()

    def record(self, agent):
        print '[Cancun] Audio Record'
        self.voicesynthetizer.speechit("Modulo de Audio, Grabacion")
        self.voicesynthetizer.speechit("Presione su ptt y hable por los proximos 5 segundos")
        if agent == 'nexiwave':
                status, output = commands.getstatusoutput("arecord -vv -f cd -d 5 " + self.audiofile)
        elif agent == 'google':
                status, output = commands.getstatusoutput("arecord -d 5 -f S16_LE --rate 16000 " + self.audiofile)

    def play(self, agent):
        print '[Cancun] Audio Play'
        self.voicesynthetizer.speechit("Modulo de Audio, Reproduccion")
        self.voicesynthetizer.speechit("Esto es lo que grabamos en 5 segundos")
        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofile)
        self.pushtotalk.closeport()
        self.voicesynthetizer.speechit("Esto es lo traducido de voz a texto")
        if agent == 'nexiwave':
                self.voicetospeech.nexiwave(self.audiofile)
        elif agent == 'google':
                output = self.voicetospeech.google(self.audiofile)
                print output
        status, output = commands.getstatusoutput("rm " + self.audiofile)

if __name__ == '__main__':

    mytest = Caudio()
    mytest.record()
    mytest.play()
