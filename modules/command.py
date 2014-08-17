#!/usr/bin/python

import commands
import json
import re

from core.voicecommand import VoiceCommand
from core.voicesynthetizer import VoiceSynthetizer
from core.voicetospeech import VoiceToSpeech
from core.pushtotalk import PushToTalk

from modules.clock import Clock
from modules.identification import Identification
from modules.weather import Weather
from modules.messages import Messages
from modules.twitterc import TwitterC

class Command(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.voicesynthetizer = voicesynthetizer
        self.voicecommand = VoiceCommand(self.voicesynthetizer)

        self.clock = Clock(voicesynthetizer)
        self.identification = Identification(voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.twitterc = TwitterC(self.voicesynthetizer)

    def presentation(self):
        print '[Cancun] Command Presentation'
        self.voicesynthetizer.speechit("Modulo experimental de comandos por voz")
        self.voicesynthetizer.speechit("Funciones disponibles: identificacion, hora, fecha, clima, estaciones y sismologia")
        self.voicesynthetizer.speechit("Dinos la funcion en los proximos 5 segundos")

    def parse(self, output):

        if re.search(r'hola', output, re.M|re.I) or re.search(r'cancun', output, re.M|re.I):
            print 'saludos'
            self.voicesynthetizer.speechit("Hola!, no se quien eres pero mucho gusto")

        if re.search(r'identif', output, re.M|re.I):
            print '[Cancun] Command Identification'
            self.voicesynthetizer.speechit("Nos has pedido identificarnos")
            self.identification.identify()
        elif re.search(r'hora', output, re.M|re.I):
            print '[Cancun] Command Hour'
            self.voicesynthetizer.speechit("Nos has pedido la hora")
            self.clock.hour()
        elif re.search(r'fecha', output, re.M|re.I):
            print '[Cancun] Command Date'
            self.voicesynthetizer.speechit("Nos has pedido la fecha")
            self.clock.date()
        elif re.search(r'clima', output, re.M|re.I):
            print '[Cancun] Command Weather'
            self.voicesynthetizer.speechit("Nos has pedido el reporte del clima")
            self.weather.report()
        elif re.search(r'estaciones', output, re.M|re.I):
            print '[Cancun] Command Stations'
            self.voicesynthetizer.speechit("Nos has pedido las estaciones en el area")
            self.messages.stations()
        elif re.search(r'sismo', output, re.M|re.I):
            print '[Cancun] Command Sismic'
            self.voicesynthetizer.speechit("Nos has pedido el reporte sismologico")
            self.twitterc.sismologicomx()
        else:
            print '[Cancun] Command? Unknown!'
            self.voicesynthetizer.speechit("Como que no entendimos tu comando!")

    def execute(self):
        self.presentation()
        self.voicecommand.record('5')
        output = self.voicecommand.decode('True')
        self.parse(output)

    def background(self):
        print '[Cancun] Background Started'
	while True:
	        self.voicecommand.record('5')
        	output = self.voicecommand.decode('False')
		self.parse(output)
        #if re.search(r'hola', output, re.M|re.I):
        #     self.voicesynthetizer.speechit("Hola!, soy el proyecto Cancun")
        #else:
        #     print 'Negativo'
        print '[Cancun] Background Stopped'

if __name__ == '__main__':

    mytest = Commands()
    mytest.record()
    mytest.play()
