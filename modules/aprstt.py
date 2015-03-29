#!/usr/bin/python

import ConfigParser
import os
import random
import string
import sys

from core.aprsnet import AprsNet
from core.voicesynthetizer import VoiceSynthetizer
from core.phonetic import Phonetic

from modules.aprstracker import AprsTracker

class Aprstt(object):

    def __init__(self, voicesynthetizer):

        self.aprs = AprsNet()
        self.phonetic = Phonetic()

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/aprstt.config"
        self.conf.read(self.path)

        self.aprstracker =  AprsTracker(voicesynthetizer)
        self.speaker = voicesynthetizer

    def dtmf_replace(self, pair):
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

    def process_number(self, number):
        
        def is_number(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        #Loop through pairs and if repeating digit, return digit, otherwise translate.
        translated_number = ""
        if number[0] == "A": # This is a callsign, so decode it.
            pairstart = True
            for p in range(1,(len(number) - 3)):
                nextchar = number[p+1]
                if ( is_number(number[p]) and not is_number(nextchar)): # Valid number letter pair
                    newpair = number[p] + nextchar
                    print newpair
                    translated_number = translated_number + self.dtmf_replace(newpair)
                elif (is_number(number[p]) and is_number(nextchar)): # Valid number.
                    translated_number = translated_number + number[p] # This is for the callsign number
                else:
                    print("Mid Pair!")
            return translated_number
        else:
            return False

    def key_composition(self, string):
        message = None
        callsign = None
        if '*' in string:
            string = string.split('*')
            message = string[0]
            callsign = string[1]
        return message, callsign

    def keytype_get_aprstt(self, string):
        return self.process_number(string)

    def keytype_get(self, string):
        datafields = {'PP': 'callsign', 'PS': 'position', 'SP': 'status', 'SS': 'message'}
        keytype = string[:2]
        return datafields.get(keytype)

    def keytype_translate(self, keytype):
        keytypes = {'callsign': 'Indicativo', 'position': 'Posicion', 'status': 'Estado', 'message': 'Mensaje'}
        return keytypes.get(keytype)

    def user_get(self, string):
        user = string[2:4]
        if string[4:5] == '0':
            generic = True
        else:
            generic = False
        return user, generic

    def command_get(self, generic, string):
        if generic:
             request = string[5:]
        else:
             request = string[4:]
        return request

    def callsign_decode(self, string):
        string = string[1:-1:]
        try:
            if len(string) > 5:
                self.callsign_decoded = self.conf.get("long", string)
            else:
                self.callsign_decoded = self.conf.get("short", string)
        except:
            self.speaker.speechit("Indicativo no valido")
            sys.exit(1)

        return self.callsign_decoded

    def position_decode(self, string):
        return string[1::].upper()

    def status_decode(self, string):
        return string[1::].upper()

    def city_randomposition(self):
        city = self.conf.get("general", "city")
        # Position Format 2036.96N/10324.46W
        randomxn = random.randint(00,99)
        randomxw = random.randint(00,99)

        if city == 'guadalajara':
            # Coordinates 204200N 2034.00N 10326.00N 10314.00N
            randomn = random.randint(34,42)
            randomw = random.randint(14,26)
            return '20' + str(randomn) + '.' + str(randomxn).zfill(2) + 'N/103' + str(randomw) + '.' + str(randomxw).zfill(2) + 'W'
        if city == 'leon':
            # Coordinates 211000N 216.00N 10144.00N 10138.00N
            randomn = random.randint(06,10)
            randomw = random.randint(38,44)
            return '21' + str(randomn).zfill(2) + '.' + str(randomxn).zfill(2) + 'N/101' + str(randomw) + '.' + str(randomxw).zfill(2) + 'W'

    def query(self, string):

        print '[Cancun] APRS Touch Tone | ' + string

        callsign = self.keytype_get_aprstt(string)
        if callsign:
            self.speaker.speechit("Bienvenido " + ' '.join(self.phonetic.decode(callsign)))
            callsignmobile = callsign + '-9'
            callsignexperimental = callsign + '-15'
            self.aprstracker.localize(callsignmobile)
            self.aprs.address_set(callsignexperimental)
            self.aprs.position_set(self.city_randomposition())
            self.aprs.send_message("Cancun Project APRS Touch Tone Basic Implementation, Random Position")

        return

        if self.keytype_get(string) is 'callsign':
            user, generic = self.user_get(string)
            callsign = self.conf.get("users", user)
            self.speaker.speechit("Estacion " + ' '.join(self.phonetic.decode(callsign)))

        command = self.command_get(generic, string)
        if generic:
            user = 'generic'
        else:
            user = callsign

        messagetype = self.keytype_translate(self.keytype_get(command[0:2]))
        messagenumber = command[2:4]
        message = messagetype + ' ' + messagenumber
        message_file = self.conf.get(user, command)
        message = message + ' ' + message_file
        self.speaker.speechit(message)
        aprs_message = callsign.upper() + " " + message
        self.aprs.send_message(aprs_message)

        return

if __name__ == '__main__':

    test = Aprstt("temp")
