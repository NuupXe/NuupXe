#!/usr/bin/python

import random

from core.camera import Camera
from core.phonetic import Phonetic
from core.randomizer import randomize
from core.twitterc import TwitterC

class PoCTwitter(object):

    def __init__(self, voicesynthetizer):

	self.camera = Camera(voicesynthetizer)
        self.phonetic = Phonetic()
	self.twitterc = TwitterC('twython')
        self.voicesynthetizer = voicesynthetizer

    def execute(self):
        self.camera.execute()
        message = randomize(6) + ' #ProyectoCancun '
        media='output/camerapygame.jpg'
        self.twitterc.timeline_set(message, media)
        message = "Foto en twitter.com/ " + ' arjac cancun'
        self.voicesynthetizer.speechit(message)
        message = ' '.join(self.phonetic.decode("arjaccancun"))
        self.voicesynthetizer.speechit(message)
