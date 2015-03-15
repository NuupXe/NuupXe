#!/usr/bin/python

import random

from core.camera import Camera
from core.phonetic import Phonetic
from core.twitterc import TwitterC
from core.utilities import Randomizer

class Selfie(object):

    def __init__(self, voicesynthetizer):

	self.camera = Camera(voicesynthetizer)
        self.phonetic = Phonetic()
	self.twitterc = TwitterC('twython')
        self.voicesynthetizer = voicesynthetizer

    def get(self):
        self.camera.execute()
        message = Randomizer(2) + ' #HamRadio #Hamr #ArejXe #ProyectoCancun #Selfie'
        message = message + ' Voice Experimental Station ... Visit me @ https://github.com/xe1gyq/cancun'
        media='output/camerapygame.jpg'
        self.twitterc.timeline_set(message, media)
        message = "Hola! Mi selfie en twitter.com/ " + ' arjac cancun'
        self.voicesynthetizer.speechit(message)
        message = ' '.join(self.phonetic.decode("arjaccancun"))
        self.voicesynthetizer.speechit(message)

# End of File
