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

from core.alive import alive
from core.aprsfi import AprsFi
from core.aprsnet import AprsNet
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

class Weather(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'Weather'
        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()
        self.aprsnet = AprsNet()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.agent = self.conf.get("weather", "agent")

        self.speaker = voicesynthetizer

    def aprspacket(self):

        self.aprsnet.send_packet("XE1GYQ-13>APRS,TCPIP*,qAS,XE1GYQ-10:@232353z2036.96N/10324.58W_000/000g000t000r000p000P000h00b00000NuupXe Weather Station")

    def aprsfi_service(self):

        print '[NuupXe] Weather aprs.fi'

        callsign = self.conf.get("weather", "aprsficallsign")
        location = self.conf.get("weather", "aprsfilocation")

        self.aprsfi.callsignset(callsign)
        self.aprsfi.dataset('wx')
        data = self.aprsfi.query()

        for entry in data['entries']:

            message = "Reporte del clima en la ciudad de " + location
            message = message + ", Datos de a p r s punto fi"
            message = message + ", Estacion meteorologica, " + ' '.join(self.phonetic.decode(callsign))
            message = message + ", Temperatura " + entry['temp'] + " grados centigrados"
            message = message + ", Humedad relativa " + entry['humidity'] + " por ciento"
            message = message + ", Presion Atmosferica " + entry['pressure'] + " milibares"
            message = message + ", Direccion del viento " + entry['wind_direction'] + " grados"
            message = message + ", Velocidad del viento " + entry['wind_speed'] + " metros por segundo"
            message = message + ", Rafagas de " + entry['wind_gust'] + " metros por segundo"
            message = message + ", Precipitacion pluvial " + entry['rain_1h'] + " milimetros"
            self.speaker.speechit(message)
            self.message = message

    def yahoo(self):

        print '[NuupXe] Weather Yahoo'

        location = self.conf.get("weather", "location")
        result = pywapi.get_weather_from_yahoo(location, 'metric')

        message = "Reporte del Clima en " + result['location']['city']
        message = message + ", Temperatura " + result['condition']['temp'] + " grados centigrados"
        message = message + ", Presion Atmosferica " + result['atmosphere']['pressure'] + " milibares"
        message = message + ", Visibilidad " + result['atmosphere']['visibility'] + " kilometros"
        message = message + ", Humedad " + result['atmosphere']['humidity'] + " por ciento"
        message = message + ", El Sol se oculta a las " + result['astronomy']['sunset']
        self.speaker.speechit(message)
        self.message = message

    def noaa(self):

        print '[NuupXe] Weather NOAA'

        location = self.conf.get("weather", "location")
        result = pywapi.get_weather_from_noaa('MMGL')

        message = "Reporte del Clima"
        message = message + ", Temperatura " + result['temp_c'] + " grados centigrados"
        message = message + ", Humedad " + result['relative_humidity'] + " por ciento"
        self.speaker.speechit(message)
        self.message = message

    def report(self):

        if self.agent == "aprsfi":
                self.aprsfi_service()
        elif self.agent == "yahoo":
                self.yahoo()
        elif self.agent == "noaa":
                self.noaa()

        self.aprspacket()
        alive(modulename=self.modulename + 'Report', modulemessage=self.message)

    def temperature(self):

        location = self.conf.get("weather", "location")
        result = pywapi.get_weather_from_yahoo(location, 'metric')

        message = "Temperatura en " + result['location']['city'] + " "
        self.speaker.speechit(message + result['condition']['temp'] + " grados centigrados")
        alive(self.modulename + 'Temperature')

# End of File
