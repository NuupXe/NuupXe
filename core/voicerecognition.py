#!/usr/bin/python

import subprocess
import logging
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

        command = "rm " + self.audiofilewav
        subprocess.call(command, shell=True)
        command = "rm " + self.audiofileflac
        subprocess.call(command, shell=True)

    def languageset(self, language):

        logging.info('Voice Recognition Language Set')

        self.language = language
        self.speechrecognition.languageset(self.language)

    def filegetname(self):

        logging.info('Voice Recogntion File Get Name')

        return self.audiofilewav

    def record(self):

        logging.info('Voice Recognition Record')

        if self.agent == 'nexiwave':
            command = 'arecord -vv -f cd -d 5 ' + self.audiofilewav
            subprocess.call(command, shell=True)
        elif self.agent == 'google':
            self.voice.record()
            command = "flac -f -o " + self.audiofileflac + " --channels=1 --sample-rate=48000 " + self.audiofilewav
            subprocess.call(command, shell=True)

    def recognize(self, speech):

        logging.info('Voice Recognition Decode')

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
