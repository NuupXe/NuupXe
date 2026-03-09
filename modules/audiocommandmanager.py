#!/usr/bin/python

import subprocess
import logging
import re

from core.alive import alive
from core.voicerecognition import VoiceRecognition
from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather
from modules.querymaster import QueryMaster

class AudioCommandManager(object):

    def __init__(self, voicesynthesizer):

        self.modulename = 'VoiceCommand'
        self.output = ""
        self.voicesynthesizer = voicesynthesizer
        self.voicerecognition = VoiceRecognition(self.voicesynthesizer)

        self.clock = Clock(voicesynthesizer)
        self.identification = Identification(voicesynthesizer)
        self.weather = Weather(self.voicesynthesizer)
        self.querymaster = QueryMaster(self.voicesynthesizer)

    def presentation(self):

        logging.info('Voice Command Presentation')
        self.voicesynthesizer.speech_it("Hola! Como puedo ayudarte?")

    def decode(self, output):

        logging.info('Voice Command Decode')

        if re.search(r'coman', output, re.M|re.I) or re.search(r'disponi', output, re.M|re.I):
            logging.info('Voice Command Decode Available Commands')
            self.voicesynthesizer.speech_it("Comandos Disponibles? Identificacion, Hora, Fecha, Clima")
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
            self.weather.weather_report()
        elif re.search(r'tempe', output, re.M|re.I) or re.search(r'tura', output, re.M|re.I):
            logging.info('Voice Command Decode Temperature')
            self.weather.weather_temperature()
        elif re.search(r'pregun', output, re.M|re.I) or re.search(r'gunta', output, re.M|re.I):
            logging.info('Voice Command Decode Query master')
            self.querymaster.listen()
        else:
            logging.error('Voice Command Unknown!')
            self.voicesynthesizer.speech_it("No entendimos tu comando!")

    def listen(self):

        logging.info('Voice Command Listen')
        self.presentation()
        self.voicerecognition.record()
        output = self.voicerecognition.recognize('False')
        self.decode(output)
        alive(modulename=self.modulename, modulemessage=' Command ' + output.capitalize())

    def background(self):

        logging.info('Voice Command Background')
        while True:
                self.voicerecognition.record()
                output = self.voicerecognition.recognize('False')
                if re.search(r'canc', output, re.M|re.I):
                    self.voicesynthesizer.speech_it("Alguien me hablo?. Soy NuupXe... Hasta pronto!")
                    break
                print(output)

# Enf of File
