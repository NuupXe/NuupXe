#!/usr/bin/python

import commands
import ConfigParser
import logging

from core.alive import alive
from core.pushtotalk import PushToTalk

class SSTV(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'SSTV @Bing'
        self.modulepicture = 'output/radioclub.jpg'
        self.voicesynthetizer = voicesynthetizer
        self.pushtotalk = PushToTalk()

    def setup(self):

        logging.info('SSTV Setup')

    def download(self):

        status, output = commands.getstatusoutput('python core/bing.py')
        status, output = commands.getstatusoutput('convert -resize 320x256\! output/bing.jpg output/iotd.jpg')
        alive(modulename=self.modulename, modulemessage=None, media='output/bing.jpg')

    def decode(self):

        logging.info('SSTV Decode')
        self.setup()
        try:
            self.voicesynthetizer.speechit("Modulo Experimental de Television de Barrido Lento, Modo Martin Uno, Procesando la imagen!")
            self.picture()
            status, output = commands.getstatusoutput('python -m pysstv --mode MartinM1 --vox output/iotd.jpg output/sstv.wav')
            self.voicesynthetizer.speechit("Imagen lista! Comenzamos con la transmision en Modo Martin Uno")
            self.pushtotalk.openport()
            status, output = commands.getstatusoutput('aplay output/sstv.wav')
            self.pushtotalk.closeport()
            alive(modulename=self.modulename, modulemessage=None, media='output/bing.jpg')
        except:
            logging.error('SSTV Decode Error')

# End of File
