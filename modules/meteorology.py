#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re
import unicodedata
import string
import sys
import feedparser
import threading

from core.twitterc import TwitterC

state = {'CHIS': 'Chiapas', 'NL': 'Nuevo Leon', 'VER': 'Veracruz',
        'JAL': 'Jalisco', 'OAX': 'Oaxaca', 'GRO': 'Guerrero',
        'BC': 'Baja California', 'SON': 'Sonora', 'TX': 'Texas',
	'Temp': 'Temperatura', 'DGO': 'Durango', 'Dgo': 'Durango',}

class Meteorology(object):

    def __init__(self, voicesynthetizer):

	self.twitterc = TwitterC('twython')

        self.voicesynthetizer = voicesynthetizer

    def conagua_clima(self):

        logging.info('Meteorology Conagua Clima')
        self.voicesynthetizer.speechit('Servicio Meteorologico Nacional, Comision Nacional del Agua')

        tstatus = self.twitterc.timeline_get('conagua_clima', 3)
        for status in tstatus:
            break
            status['text'] = status['text']
            status['text'] = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
            URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
            status['text'] = status['text'].replace("#", "")
            status['text'] = status['text'].replace("en:", "")
            status['text'] = status['text'].replace("h:", " Horas ")
            status['text'] = status['text'].replace("hrs:", " Horas ")
            status['text'] = status['text'].replace(" h ", " horas ")
            status['text'] = status['text'].replace("C.", " Grados ")
            status['text'] = status['text'].replace("SMN", " Servicio Meteorologico Nacional ")
            status['text'] = status['text'].replace("km/h", " Kilometros por hora ")
            status['text'] = status['text'].replace("TempMin", " Temperatura Minima ")
            status['text'] = status['text'].replace("TempMax", " Temperatura Maxima ")
            pattern = re.compile(r'\b(' + '|'.join(state.keys()) + r')\b')
            status['text'] = pattern.sub(lambda x: state[x.group()], status['text'])
            try:
                self.voicesynthetizer.speechit(status['text'])
            except:
                logging.info('Meteorology Conagua Clima Error')
        self.voicesynthetizer.speechit('Mas informacion en twitter.com/conagua_clima')

# End of File
