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
	'JAL': 'Jalisco', 'OAX': 'Oaxaca'}

class Meteorology(object):

    def __init__(self, voicesynthetizer):

	self.twitterc = TwitterC()

        self.voicesynthetizer = voicesynthetizer

    def remove_accents(self, input_str):
                nkfd_form = unicodedata.normalize('NFKD', input_str)
                only_ascii = nkfd_form.encode('ASCII', 'ignore')
                return only_ascii

    def conagua_clima(self):
        print '[Cancun] Meteorology'
        #self.voicesynthetizer.speechit('Servicio Meteorologico Nacional, Comision Nacional del Agua')

        tstatus = self.twitterc.timeline_get('conagua_clima', 1)
        #sismo = 'False'
        for status in tstatus:
            #print status
            #print status.text.partition(' ')[0]
            #    status.text = status.text.replace("Loc", "Localizacion")
            #    status.text = status.text.replace("CD", "Ciudad")
            #    status.text = status.text.replace("Lat", "Latitud")
            #    status.text = status.text.replace("Lon", "Longitud")
            #    status.text = status.text.replace("Pf", "Profundidad")
            #    pattern = re.compile(r'\b(' + '|'.join(state.keys()) + r')\b')
            #status.text = pattern.sub(lambda x: state[x.group()], status.text)
            status.text = self.remove_accents(status.text)
            #print re.sub(r'^https?:\/\/*.*[\r\n]*', '', status.text)
            status.text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status.text)
            URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', status.text)
            print URLless_string
            print status.text
            #status.text = re.sub(r'http:\/\/*[\r\n]*', '', status.text)
            #status.text = "\"" + status.text + "\""
            self.voicesynthetizer.speechit(status.text)
            #print status.text
            #for single in status.text:
            #    print single
                #self.voicesynthetizer.speechit(status.text)
            #    sismo = 'True'
        #if sismo == 'False':
        #    self.voicesynthetizer.speechit("No se encontraron sismos en las ultimas horas")

if __name__ == '__main__':

    mytest = Meteorology("google")
    mytest.conagua_clima()
