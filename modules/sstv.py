#!/usr/bin/python

import subprocess
import configparser
import logging

from core.alive import alive
from core.pushtotalk import PushToTalk
from core.imagecreator import ImageCreator

class SSTV(object):

    def __init__(self, voicesynthetizer):
        self.modulename = 'SSTV'
        self.modulepicture = 'output/image.jpg'
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def setup(self):
        logging.info('SSTV Setup')

    def resize(self):
        subprocess.call('convert -resize 320x256\! /tmp/image.jpg /tmp/iotd.jpg', shell=True)

    def decode(self):
        logging.info('SSTV Decode')
        self.setup()
        self.voicesynthetizer.speech_it("Modulo Experimental de Television de Barrido Lento, Modo Martin Uno, Procesando la imagen!")
        image_creator = ImageCreator(service='openai', market='en-US', resolution='1920x1080', output_directory='output/image.jpg')
        image_creator.create_image()
        self.resize()
        subprocess.call('python -m pysstv --mode MartinM1 --vox /tmp/iotd.jpg /tmp/sstv.wav', shell=True)
        self.voicesynthetizer.speech_it("Imagen lista! Comenzamos con la transmision en Modo Martin Uno")
        self.pushtotalk.open_port()
        subprocess.call('aplay /tmp/sstv.wav', shell=True)
        self.pushtotalk.close_port()
        #alive(modulename=self.modulename, modulemessage=None, media='output/bing.jpg')

# End of File
