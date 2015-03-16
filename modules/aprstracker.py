#!/usr/bin/python

import ConfigParser
import feedparser
import logging
import os
import pywapi
import string
import sys
import time
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

class AprsTracker(object):

    def __init__(self, voicesynthetizer):

        self.phonetic = Phonetic()
        self.aprsfi = AprsFi()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)

        self.speaker = voicesynthetizer
        self.callsign = 'XE1GQP-9'

    def clock(self, aprstime):

        logging.info('Aprs Tracker Clock')
        weekday = days[time.strftime("%A", time.gmtime(int(aprstime)))]
        day = time.strftime("%d", time.gmtime(int(aprstime))).lstrip('0')
        month = months[time.strftime("%B", time.gmtime(int(aprstime)))]
        year = time.strftime("%Y", time.gmtime(int(aprstime)))
        return weekday, day, month, year

    def query(self):

        logging.info('Aprs Tracker Query')

        self.aprsfi.callsignset(self.callsign)
        self.aprsfi.dataset('loc')
        data = self.aprsfi.query()
        logging.info(data)

        for entry in data['entries']:
            self.speaker.speechit("Seguimiento por voz de estaciones en a p r s punto f i")
            self.speaker.speechit("Estacion , " + ' '.join(self.phonetic.decode(self.callsign)))
            weekday, day, month, year = self.clock(entry['lasttime'])
            lasttimeseen = "Ultima vez visto " + weekday + ' ' + day + ' de ' + month + ' del ' + year
            self.speaker.speechit(lasttimeseen)
            self.speaker.speechit("Velocidad " + str(entry['speed']) + " Km/h")
            self.speaker.speechit("Altitud " + str(entry['altitude']) + " metros" )
            results = Geocoder.reverse_geocode(float(entry['lat']), float(entry['lng']))
            logging.info(results)
            try:
                self.speaker.speechit("Calle " + results[0].route)
                self.speaker.speechit("Colonia " + results[0].political)
                if results[0].administrative_area_level_2:
                    self.speaker.speechit("Municipip " + results[0].administrative_area_level_2)
                elif results[0].locality:
                    self.speaker.speechit("Municipio " + results[0].locality)
                self.speaker.speechit("Estado " + results[0].administrative_area_level_1)
                self.speaker.speechit("Pais " + results[0].country)
            except:
                pass

# End of File
