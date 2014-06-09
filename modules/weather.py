#!/usr/bin/python

import ConfigParser
import time
import feedparser
import os

from core.voicesynthetizer import VoiceSynthetizer

class Weather(object):

    def __init__(self, voicesynthetizer):

        print '[Cancun] Weather'

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.configuration"
        self.conf.read(self.path)

        self.agent = self.conf.get("weather", "agent")

        self.speaker = voicesynthetizer

    def yahoo(self):

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

    def report(self):

        if self.agent == "yahoo":
                self.yahoo()

        return

if __name__ == '__main__':

    test = Weather("temp")
    test.report()
