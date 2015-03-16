#!/usr/bin/python

import commands
import logging
import re

from core.voicerecognition import VoiceRecognition

from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather

class VoiceCommand(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.voicesynthetizer = voicesynthetizer
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)

        self.clock = Clock(voicesynthetizer)
        self.identification = Identification(voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

    def presentation(self):

        logging.info('Voice Command Presentation')
        self.voicesynthetizer.speechit("Hola! Como puedo ayudarte?")

    def decode(self, output):

        logging.info('Voice Command Decode')

        if re.search(r'coman', output, re.M|re.I) or re.search(r'disponi', output, re.M|re.I):
            logging.info('Voice Command Decode Available Commands')
            self.voicesynthetizer.speechit("Comandos Disponibles? Identificacion, Hora, Fecha, Clima")
        elif re.search(r'identif', output, re.M|re.I):
            logging.info('Voice Command Decode Identification')
            self.identification.identify()
        elif re.search(r'hora', output, re.M|re.I):
            logging.info('Voice Command Decode Hour')
            self.clock.hour()
        elif re.search(r'fecha', output, re.M|re.I):
            logging.info('Voice Command Decode Date')
            self.clock.date()
        elif re.search(r'clima', output, re.M|re.I):
            logging.info('Voice Command Decode Weather')
            self.weather.report()
        else:
            logging.error('Voice Command Unknown!')
            self.voicesynthetizer.speechit("No entendimos tu comando!")

    def listen(self):

        logging.info('Voice Command Listen')
        self.presentation()
        self.voicerecognition.record()
        output = self.voicerecognition.recognize('False')
        self.decode(output)

    def background(self):

        logging.info('Voice Command Background')
	while True:
	        self.voicerecognition.record()
        	output = self.voicerecognition.recognize('False')
                if re.search(r'canc', output, re.M|re.I):
                    self.voicesynthetizer.speechit("Alguien me hablo?. Soy el proyecto Cancun... Hasta pronto!")
                    break
                print output

# Enf of File
