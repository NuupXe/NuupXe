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

    def decode(self):

        logging.info('SSTV Decode')
        self.setup()
        try:
            self.voicesynthetizer.speechit("Modulo Experimental de Television de Barrido Lento, Modo Martin Uno, Procesando la imagen!")
            status, output = commands.getstatusoutput('python core/bing.py')
            status, output = commands.getstatusoutput('convert -resize 320x256\! output/bing.jpg output/radioclub.jpg')
            status, output = commands.getstatusoutput('python -m pysstv --mode MartinM1 --vox output/radioclub.jpg output/sstv.wav')
            self.voicesynthetizer.speechit("Imagen lista! Comenzamos con la tranmision en Modo Martin Uno")
            self.pushtotalk.openport()
            status, output = commands.getstatusoutput('aplay output/sstv.wav')
            self.pushtotalk.closeport()
            alive(modulename=self.modulename, media='output/bing.jpg')
        except:
            logging.error('Cannot decode file')

# End of File
