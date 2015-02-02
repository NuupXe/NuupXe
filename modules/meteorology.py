# -*- coding: utf-8 -*-
#!/usr/bin/python

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

    def remove_accents(self, input_str):
                nkfd_form = unicodedata.normalize('NFKD', input_str)
                only_ascii = nkfd_form.encode('ASCII', 'ignore')
                return only_ascii

    def conagua_clima(self):
        print '[Cancun] Meteorology'
        self.voicesynthetizer.speechit('Servicio Meteorologico Nacional, Comision Nacional del Agua')

        tstatus = self.twitterc.timeline_get('conagua_clima', 5)
        for status in tstatus:
            status['text'] = self.remove_accents(status['text'])
            status['text'] = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
            URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status['text'])
            status['text'] = status['text'].replace("#", "")
            status['text'] = status['text'].replace("h:", "Horas")
            status['text'] = status['text'].replace("C.", "Grados")
            status['text'] = status['text'].replace("km/h", "Kilometros por hora")
            pattern = re.compile(r'\b(' + '|'.join(state.keys()) + r')\b')
            status['text'] = pattern.sub(lambda x: state[x.group()], status['text'])
            print status['text']
            self.voicesynthetizer.speechit(status['text'])

if __name__ == '__main__':

    mytest = Meteorology("google")
    mytest.conagua_clima()
