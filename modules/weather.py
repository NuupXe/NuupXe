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

	self.pp = pprint.PrettyPrinter(indent=4)

    def personal(self):

        self.aprsnet.send_packet("XE1GYQ-13>APRS,TCPIP*,qAS,XE1GYQ-10:@232353z2036.96N/10324.58W_000/000g000t000r000p000P000h00b00000Cancun Project Experimental Weather Station")

    def aprsfi_service(self):

        print '[Cancun] Weather aprs.fi'
        callsign = self.conf.get("weather", "aprsficallsign")
        location = self.conf.get("weather", "aprsfilocation")

        self.aprsfi.callsign_set(callsign)
        self.aprsfi.data_set('wx')
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

        yahoocityid = self.conf.get("weather", "yahoocityid")
        result = pywapi.get_weather_from_yahoo(yahoocityid, 'metric')

        self.speaker.speechit("Reporte del clima en la ciudad de " + result['location']['city'])
        self.speaker.speechit("Temperatura, " + result['condition']['temp'] + " grados centigrados")
        self.speaker.speechit("Presion Atmosferica, " + result['atmosphere']['pressure'] + " milibares")
        self.speaker.speechit("Visibilidad, " + result['atmosphere']['visibility'] + " kilometros")
        self.speaker.speechit("Humedad, " + result['atmosphere']['humidity'] + " por ciento")
        self.speaker.speechit("El Sol se oculta a las " + result['astronomy']['sunset'])

    def noaa(self):

        print '[Cancun] Weather NOAA'

        #pp = pprint.PrettyPrinter(indent=4)
        noaa_result = pywapi.get_weather_from_noaa('MMGL')
        #pp.pprint(noaa_result)
        noaa_text = "Los resultados NOAA son: " + string.lower(noaa_result['weather']) + " y " + noaa_result['temp_c'] + "C ahora en Guadalajara"
        print noaa_text
	self.speaker.speechit(noaa_text)
        
    def report(self):

        if self.agent == "aprsfi":
                self.aprsfi_service()
        elif self.agent == "yahoo":
                self.yahoo()
        elif self.agent == "noaa":
                self.noaa()

        self.personal()

        return

if __name__ == '__main__':

    test = Weather("temp")
    test.report()
