#!/usr/bin/python

import commands
import json
import re

from core.voicesynthetizer import VoiceSynthetizer
from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

class Caudio(object):

    def __init__(self, voicesynthetizer):

        self.audiofilewav = "audio.wav"
        self.audiofileflac = "audio.flac"
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
                #status, output = commands.getstatusoutput("arecord -d 5 -f S16_LE --rate 16000 " + self.audiofile)
                #status, output = commands.getstatusoutput("arecord -d 5 -f dat -t wav -r 48000 -c 2 | flac -f -o " + self.audiofile + " - --channels=2 --sample-rate=44100")
                status, output = commands.getstatusoutput("arecord -d 5 -f dat -t wav -r 48000 -c 2 " + self.audiofilewav)
                status, output = commands.getstatusoutput("flac -f -o " + self.audiofileflac + " --channels=2 --sample-rate=44100 " + self.audiofilewav)
		print output

    def play(self, agent):
        print '[Cancun] Audio Play'
        self.voicesynthetizer.speechit("Modulo de Audio, Reproduccion")
        self.voicesynthetizer.speechit("Esto es lo que grabamos en 5 segundos")
        self.pushtotalk.openport()
        status, output = commands.getstatusoutput("aplay " + self.audiofilewav)
        #status, output = commands.getstatusoutput("mplayer " + self.audiofileflac)
        self.pushtotalk.closeport()
        self.voicesynthetizer.speechit("Esto es lo traducido de voz a texto")
        if agent == 'nexiwave':
                self.voicetospeech.nexiwave(self.audiofile)
        elif agent == 'google':
                output = self.voicetospeech.google(self.audiofileflac)
                self.parse(output)
        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
        status, output = commands.getstatusoutput("rm " + self.audiofileflac)

    def parse(self, output):
        print output
        if re.search(r'conectar', output, re.M|re.I):
            print 'conectar'
            self.voicesynthetizer.speechit("Comando Conectar Activado")
        elif re.search(r'saludos', output, re.M|re.I):
            print 'saludos'
            self.voicesynthetizer.speechit("Comando Saludos Activado, Saludos radioaficionado")
        else:
            print 'que dijiste?'
        

if __name__ == '__main__':

    mytest = Caudio()
    mytest.record()
    mytest.play()
