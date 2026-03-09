#!/usr/bin/python

import subprocess
import time

from core.alive import alive
from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.voice import Voice

class VoiceMail(object):

    def __init__(self, voicesynthesizer):

        self.modulename = 'VoiceMail'
        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.voice = Voice()

        self.voicesynthesizer = voicesynthesizer
        self.audiofileuser = 'output/voicemailuser'
        self.audiofilemessage = 'output/voicemailmessage'

    def record(self):
        print('[NuupXe] Voice Mail Record')
        self.voice.record()

    def play(self):
        print('[NuupXe] Voice Mail Play')
        self.pushtotalk.open_port()
        self.voice.play()
        self.pushtotalk.close_port()

    def run(self, dtmf):
        print('[NuupXe] Voice Mail Run')

        if dtmf:
            message = "Codigo recibido " + dtmf
            self.voicesynthesizer.speech_it(message)
        self.voicesynthesizer.speech_it("Identificate por favor")
        self.voice.filenameset(self.audiofileuser)
        self.record()

        self.voicesynthesizer.speech_it("Deja tu mensaje")
        self.voice.filenameset(self.audiofilemessage)
        self.record()

        self.voicesynthesizer.speech_it("Mensaje de")
        self.voice.filenameset(self.audiofileuser)
        self.play()
        self.voice.filenameset(self.audiofilemessage)
        self.play()

        alive(modulename=self.modulename, modulemessage='VoiceMail')

# End of File
