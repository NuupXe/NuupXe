#!/usr/bin/python

import ConfigParser
import time
import feedparser
import os
import pywapi
import string
import unicodedata

from pygeocoder import Geocoder
from core.aprsfi import AprsFi
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

days = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miercoles',
'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sabado',
'Sunday': 'Domingo',
}

months = {'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
'October': 'Octubre', 'November' : 'Noviembre', 'December': 'Diciembre'
}

class Tracker(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()
        #geocoder = Geocoder(api_key='MY_SIMPLE_API_KEY')

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.speaker = voicesynthetizer

    def clock(self, aprstime):
        weekday = days[time.strftime("%A", time.gmtime(int(aprstime)))]
        day = time.strftime("%d", time.gmtime(int(aprstime))).lstrip('0')
        month = months[time.strftime("%B", time.gmtime(int(aprstime)))]
        year = time.strftime("%Y", time.gmtime(int(aprstime)))
        return weekday, day, month, year

    def remove_accents(self, input_str):
        nkfd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nkfd_form.encode('ASCII', 'ignore')
        return only_ascii

    def query(self):

        print '[Cancun] Tracker aprs.fi'

        callsign = 'XE1GQP-9'
        self.aprsfi.callsign_set(callsign)
        self.aprsfi.data_set('loc')
        data = self.aprsfi.query()

        print data

        for entry in data['entries']:
            self.speaker.speechit("Seguimiento por voz de estaciones en a p r s")
            self.speaker.speechit("Datos de a p r s punto fi")
            self.speaker.speechit("Estacion , " + ' '.join(self.phonetic.decode(callsign)))
            weekday, day, month, year = self.clock(entry['lasttime'])
            self.speaker.speechit("Ultima vez visto, " + weekday + day + month + year)
            results = Geocoder.reverse_geocode(float(entry['lat']), float(entry['lng']))
            print results[0]
            self.speaker.speechit("Calle, " + self.remove_accents(results[0].route))
            self.speaker.speechit("Municipio, " + self.remove_accents(results[0].locality))
            self.speaker.speechit("Estado, " + results[0].administrative_area_level_1)

if __name__ == '__main__':

    test = Tracker("temp")
    test.query()
