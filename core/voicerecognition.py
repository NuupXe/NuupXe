#!/usr/bin/python

import commands
import time

from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.speechrecognition import SpeechRecognition
from core.voice import Voice

class VoiceRecognition(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.agent = "google"
        self.language = 'spanish'
        self.audiofilewav = "output/voicerecognition.wav"
        self.audiofileflac = "output/voicrecognition.flac"
        self.voicesynthetizer = voicesynthetizer

        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.speechrecognition = SpeechRecognition()
        self.voice = Voice()

        self.voice.filenameset(self.audiofilewav)

    def __del__(self):

        status, output = commands.getstatusoutput("rm " + self.audiofilewav)
        status, output = commands.getstatusoutput("rm " + self.audiofileflac)

    def languageset(self, language):
        self.language = language
        self.speechrecognition.languageset(self.language)

    def record(self):

        print 'Voice Command Record'

        if self.agent == 'nexiwave':
            status, output = commands.getstatusoutput("arecord -vv -f cd -d 5 " + self.audiofilewav)
        elif self.agent == 'google':
            self.voice.record()
            commands.getstatusoutput("flac -f -o " + self.audiofileflac + " --channels=1 --sample-rate=48000 " + self.audiofilewav)

    def recognize(self, speech):

        print 'Voice Command Decode'

	if speech == 'True':
            self.pushtotalk.openport()
            self.voice.play()
            self.pushtotalk.closeport()

        if self.agent == 'nexiwave':
            self.output = self.speechrecognition.nexiwave(self.audiofilewav)
        elif self.agent == 'google':
            self.output = self.speechrecognition.google(self.audiofileflac)

        return self.output

# End of File
