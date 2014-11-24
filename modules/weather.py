#!/usr/bin/python

import ConfigParser
import time
import feedparser
import os
import pywapi
import string
import json
import urllib2

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

        self.aprsnet.send_packet_raw("XE1GYQ-13>APRS,TCPIP*,qAS,XE1GYQ-10:@232353z2036.80N/10324.50W_000/000g000t000r000p000P000h00b00000Cancun Project Experimental Weather Station")

    def yahoo(self):

        print '[Cancun] Weather Yahoo'

        yahoocityid = self.conf.get("weather", "yahoocityid")
        self.url = "http://weather.yahooapis.com/forecastrss?w=" + yahoocityid  + "&u=c"

        data = feedparser.parse(self.url)

	# {'city': u'Guadalajara', 'region': u'JA', 'country': u'Mexico'}
	# {'direction': u'0', 'speed': u'0', 'chill': u'22'}
	# {'pressure': u'1008.2', 'rising': u'1', 'visibility': u'12.87', 'humidity': u'73'}
	# {'sunset': u'8:32 pm', 'sunrise': u'7:12 am'}
        
        self.location = data.feed.yweather_location
        self.wind = data.feed.yweather_wind
        self.atmosphere = data.feed.yweather_atmosphere
        self.astronomy = data.feed.yweather_astronomy

        sunrise=self.astronomy['sunrise']
        sunset=self.astronomy['sunset']

        summary=data.entries[0].summary
        temp=summary.split("High: ")
        temp=temp[1].split(" Low: ")
        self.high=temp[0]
        self.low=temp[1].split("<br />")[0]

        self.speaker.speechit("Reporte del clima en la ciudad de " + self.location['city'] + ", " + self.location['country'])
        self.speaker.speechit("Temperatura maxima, " + self.high + " grados centigrados")
        self.speaker.speechit("Temperatura minima, " + self.low + " grados centigrados")
        self.speaker.speechit("Presion Atmosferica, " + self.atmosphere['pressure'] + " milibares")
        self.speaker.speechit("Visibilidad, " + self.atmosphere['visibility'] + " kilometros")
        self.speaker.speechit("Humedad, " + self.atmosphere['humidity'] + " por ciento")
        self.speaker.speechit("El Sol se oculta a las " + self.astronomy['sunset'].replace(":", " "))

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
        if self.agent == "yahoo":
                self.yahoo()
        elif self.agent == "noaa":
                self.noaa()

        return

if __name__ == '__main__':

    test = Weather("temp")
    test.report()
