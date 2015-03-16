#!/usr/bin/python

import ConfigParser
import time
import feedparser
import os
import pywapi
import string
import json
import urllib2
import pprint

from core.aprsfi import AprsFi
from core.aprsnet import AprsNet
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

class Weather(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()
        self.aprsnet = AprsNet()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.agent = self.conf.get("weather", "agent")

        self.speaker = voicesynthetizer

    def aprspacket(self):

        self.aprsnet.send_packet("XE1GYQ-13>APRS,TCPIP*,qAS,XE1GYQ-10:@232353z2036.96N/10324.58W_000/000g000t000r000p000P000h00b00000Cancun Project Experimental Weather Station")

    def aprsfi(self):

        print '[Cancun] Weather aprs.fi'

        callsign = self.conf.get("weather", "aprsficallsign")
        location = self.conf.get("weather", "aprsfilocation")

        self.aprsfi.callsignset(callsign)
        self.aprsfi.dataset('wx')
        data = self.aprsfi.query()

        for entry in data['entries']:

            self.speaker.speechit("Reporte del clima en la ciudad de " + location)
            self.speaker.speechit("Datos de a p r s punto fi")
            self.speaker.speechit("Estacion meteorologica, " + ' '.join(self.phonetic.decode(callsign)))
            self.speaker.speechit("Temperatura, " + entry['temp'] + " grados centigrados")
            self.speaker.speechit("Humedad relativa, " + entry['humidity'] + " por ciento")
            self.speaker.speechit("Presion Atmosferica, " + entry['pressure'] + " milibares")
            self.speaker.speechit("Direccion del viento, " + entry['wind_direction'] + " grados")
            self.speaker.speechit("Velocidad del viento, " + entry['wind_speed'] + " metros por segundo")
            self.speaker.speechit("Rafagas de " + entry['wind_gust'] + " metros por segundo")
            self.speaker.speechit("Precipitacion pluvial, " + entry['rain_1h'] + " milimetros")

    def yahoo(self):

        print '[Cancun] Weather Yahoo'

        location = self.conf.get("weather", "location")
        result = pywapi.get_weather_from_yahoo(location, 'metric')

        self.speaker.speechit("Reporte del Clima en " + result['location']['city'])
        self.speaker.speechit("Temperatura, " + result['condition']['temp'] + " grados centigrados")
        self.speaker.speechit("Presion Atmosferica, " + result['atmosphere']['pressure'] + " milibares")
        self.speaker.speechit("Visibilidad, " + result['atmosphere']['visibility'] + " kilometros")
        self.speaker.speechit("Humedad, " + result['atmosphere']['humidity'] + " por ciento")
        self.speaker.speechit("El Sol se oculta a las " + result['astronomy']['sunset'])

    def noaa(self):

        print '[Cancun] Weather NOAA'

        location = self.conf.get("weather", "location")
        result = pywapi.get_weather_from_noaa('MMGL')

        self.speaker.speechit("Reporte del Clima")
        self.speaker.speechit("Temperatura, " + result['temp_c'] + " grados centigrados")
        self.speaker.speechit("Humedad, " + result['relative_humidity'] + " por ciento")
  
    def report(self):

        if self.agent == "aprsfi":
                self.aprsfi()
        elif self.agent == "yahoo":
                self.yahoo()
        elif self.agent == "noaa":
                self.noaa()

        self.aprspacket()

# End of File
