#!/usr/bin/python

import commands
import time

from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.speechrecognition import SpeechRecognition
from core.voice import Voice

class VoiceCommand(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.agent = "google"
        self.language = 'spanish'
        self.audiofilewav = "voicecommand.wav"
        self.audiofileflac = "voicecommand.flac"
        self.voicesynthetizer = voicesynthetizer

        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.speechrecognition = SpeechRecognition()
        self.voice = Voice()

        self.voice.record_filename(self.audiofilewav)

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
            print 'In voice command'
            time.sleep(1)
            while self.irlp.cosenabled() is 256:
                pass
            while self.irlp.cosenabled() is 0:
                pass
            proc = self.voice.record_start()
            while self.irlp.cosenabled() is 256:
                pass
            self.voice.record_stop(proc)
            commands.getstatusoutput("flac -f -o " + self.audiofileflac + " --channels=1 --sample-rate=48000 " + self.audiofilewav)

    def decode(self, speech):

        print 'Voice Command Decode'

	if speech == 'True':
            self.voicesynthetizer.speechit("Estamos procesando tu respuesta")
            self.pushtotalk.openport()
            self.voice.play()
            self.pushtotalk.closeport()

        if self.agent == 'nexiwave':
            self.output = self.speechrecognition.nexiwave(self.audiofilewav)
        elif self.agent == 'google':
            self.output = self.speechrecognition.google(self.audiofileflac)

        return self.output

# End of File
