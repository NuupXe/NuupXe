#!/usr/bin/python

import ConfigParser
import os
import string

from core.aprsnet import AprsNet
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

class Aprstt(object):

    def __init__(self, voicesynthetizer):

        self.aprs = AprsNet()
        self.phonetic = Phonetic()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/aprstt.config"
        self.conf.read(self.path)

        self.speaker = voicesynthetizer

    def dtmf_replace(pair):
        d = {}
        d["2A"] = "A"
        d["2B"] = "B"
        d["2C"] = "C"
        d["3A"] = "D"
        d["3B"] = "E"
        d["3C"] = "F"
        d["4A"] = "G"
        d["4B"] = "H"
        d["4C"] = "I"
        d["5A"] = "J"
        d["5B"] = "K"
        d["5C"] = "L"
        d["6A"] = "M"
        d["6B"] = "N"
        d["6C"] = "O"
        d["7A"] = "P"
        d["7B"] = "Q"
        d["7C"] = "R"
        d["7D"] = "S"
        d["8A"] = "T"
        d["8B"] = "U"
        d["8C"] = "V"
        d["9A"] = "W"
        d["9B"] = "X"
        d["9C"] = "Y"
        d["9D"] = "Z"
        return d[pair]

    def key_composition(self, string):
        message = None
        callsign = None
        if '*' in string:
            string = string.split('*')
            message = string[0]
            callsign = string[1]
        return message, callsign

    def key_type(self, string):
        # A Callsign, B Position Data, C Comment Text or Status, D Message Text
        typekey = string.split()[0][0]
        datafields = {'A': 'callsign', 'B': 'position', 'C': 'status', 'D': 'message'}
        return datafields.get(typekey)

    def callsign_decode(self, string):
        string = string[1:-1:]
        if len(string) > 5:
            self.callsign_decoded = self.conf.get("long", string)
        else:
            self.callsign_decoded = self.conf.get("short", string)
        return self.callsign_decoded

    def position_decode(self, string):
        return string[1::].upper()

    def status_decode(self, string):
        return string[1::].upper()

    def query(self, string):

        print '[Cancun] APRS TT | ' + string
        #self.speaker.speechit("Trama, " + ' '.join(self.phonetic.decode(string)))
        #self.speaker.speechit("Resultado, " + ' '.join(self.phonetic.decode(self.key_type(string))))

        if self.key_type(string) is 'callsign':
            callsign_decoded = self.callsign_decode(string.upper())
            self.speaker.speechit("Bienvenida Estacion, " + ' '.join(self.phonetic.decode(callsign_decoded)))
            self.aprs.send_packet(callsign_decoded)
        elif self.key_type(string) is 'position':
            message, callsign = self.key_composition(string)
            if callsign:
                callsign_decoded = self.callsign_decode(callsign.upper())
                self.speaker.speechit("Bienvenida Estacion, " + ' '.join(self.phonetic.decode(callsign_decoded)))
            message_decoded = self.position_decode(message)
            self.speaker.speechit("Mensaje, " + ' '.join(self.phonetic.decode(message_decoded)))
            self.aprs.send_packet(message_decoded)
        elif self.key_type(string) is 'status':
            message, callsign = self.key_composition(string)
            if callsign:
                callsign_decoded = self.callsign_decode(callsign.upper())
                self.speaker.speechit("Bienvenida Estacion, " + ' '.join(self.phonetic.decode(callsign_decoded)))
            message_decoded = self.status_decode(message)
            self.speaker.speechit("Mensaje, " + ' '.join(self.phonetic.decode(message_decoded)))
            self.aprs.send_packet(message_decoded)
        return

if __name__ == '__main__':

    test = Aprstt("temp")
