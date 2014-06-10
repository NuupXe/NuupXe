#!/usr/bin/python

import commands

from core.voicesynthetizer import VoiceSynthetizer
from core.pushtotalk import PushToTalk

class Caudio(object):

    def __init__(self, voicesynthetizer):

        self.audiofile = 'audio.wav'
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def record(self):
        print '[Cancun] Audio Record'
        self.voicesynthetizer.speechit("Modulo de Audio, Grabacion")
        self.voicesynthetizer.speechit("Presione su ptt y hable por los proximos 5 segundos")
        status, output = commands.getstatusoutput("arecord -vv -f cd -d 5 " + self.audiofile)

    def play(self):
        print '[Cancun] Audio Play'
        self.voicesynthetizer.speechit("Modulo de Audio, Reproduccion")
        self.voicesynthetizer.speechit("Esto es lo que grabamos en 5 segundos")
        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofile)
        self.pushtotalk.closeport()
        status, output = commands.getstatusoutput("rm " + self.audiofile)

if __name__ == '__main__':

    mytest = Caudio()
    mytest.record()
    mytest.play()
