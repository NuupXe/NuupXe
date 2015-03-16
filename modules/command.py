#!/usr/bin/python

import commands
import re

from core.irlp import Irlp
from core.voicerecognition import VoiceRecognition
from core.voicesynthetizer import VoiceSynthetizer
from core.pushtotalk import PushToTalk

from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather
from modules.messages import Messages
from modules.seismology import Seismology

class Command(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.voicesynthetizer = voicesynthetizer
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)

        self.clock = Clock(voicesynthetizer)
        self.identification = Identification(voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)

    def presentation(self):
        print '[Cancun] Command Presentation'
        self.voicesynthetizer.speechit("Modulo experimental de comandos por voz")
        self.voicesynthetizer.speechit("Funciones disponibles: identificacion, hora, fecha, clima y sismologia")
        self.voicesynthetizer.speechit("")

    def parse(self, output):

        if re.search(r'hola', output, re.M|re.I) or re.search(r'cancun', output, re.M|re.I):
            self.voicesynthetizer.speechit("Hola!, no se quien eres pero mucho gusto")

        if re.search(r'identif', output, re.M|re.I):
            print '[Cancun] Command Identification'
            self.identification.identify()
        elif re.search(r'hora', output, re.M|re.I):
            print '[Cancun] Command Hour'
            self.clock.hour()
        elif re.search(r'fecha', output, re.M|re.I):
            print '[Cancun] Command Date'
            self.clock.date()
        elif re.search(r'clima', output, re.M|re.I):
            print '[Cancun] Command Weather'
            self.weather.report()
        elif re.search(r'sismo', output, re.M|re.I):
            print '[Cancun] Command Seismic'
            self.seismology.SismologicoMX()
        else:
            print '[Cancun] Command? Unknown!'
            self.voicesynthetizer.speechit("No entendimos, hasta pronto!")

    def execute(self):
        self.presentation()
        self.voicerecognition.record()
        output = self.voicerecognition.recognize('False')
        print output
        self.parse(output)

    def background(self):
        print '[Cancun] Background Started'
	while True:
	        self.voicerecognition.record()
        	output = self.voicerecognition.recognize('False')
                if re.search(r'canc', output, re.M|re.I):
                    self.voicesynthetizer.speechit("Alguien me hablo?. Soy el proyecto Cancun... Hasta pronto!")
                    break
                print output
        print '[Cancun] Background Stopped'

# Enf of File
