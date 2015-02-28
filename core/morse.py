#!/usr/bin/python

import ConfigParser
import commands
import pygame
import sys
import time

from pushtotalk import PushToTalk

code = {'A': '.-',  'B': '-...',    'C': '-.-.',
    'D': '-..', 'E': '.',   'F': '..-.',
    'G': '--.', 'H': '....',    'I': '..',
    'J': '.---',    'K': '-.-', 'L': '.-..',
    'M': '--',  'N': '-.',  'O': '---',
    'P': '.--.',    'Q': '--.-',    'R': '.-.',
    'S': '...', 'T': '-',   'U': '..-',
    'V': '...-',    'W': '.--', 'X': '-..-',
    'Y': '-.--',    'Z': '--..',

    '0': '-----',   '1': '.----',   '2': '..---',
    '3': '...--',   '4': '....-',   '5': '.....',
    '6': '-....',   '7': '--...',   '8': '---..',
    '9': '----.'
    }

class Morse(object):

    def __init__(self):

        self.configuration()

    def configuration(self):
        self.message = ""
        self.oneunit = 0.5
        self.threeunits = 3 * self.oneunit
        self.sevenunits = 7 * self.oneunit
        self.morsefiles = 'morsefiles/'

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.morseagent = self.conf.get("general", "morseagent")

        if self.morseagent == 'pygame':
            pygame.init()

        self.pushtotalk = PushToTalk()

    def verify(self, message):
        keys = code.keys()
        for char in message:
            if char.upper() not in keys and char != ' ':
                sys.exit('Error the character ' + char + ' cannot be translated to Morse Code')

    def generate(self, message):

        self.pushtotalk.openport()

        if self.morseagent == 'pygame':
            self.verify(message)
            for char in message:
                if char == ' ':
                    print ' '*7,
                    time.sleep(self.sevenunits)
                else:
                    print code[char.upper()],
                    print
                    pygame.mixer.music.load(self.morsefiles + char.upper() + '_morse_code.ogg')
                    pygame.mixer.music.play()
                    time.sleep(self.threeunits)
        elif self.morseagent == 'cwpcm':
            message = 'echo ' + message + ' | /home/irlp/bin/cwpcm -sm -l 007 -p 1000 > /dev/dsp'
            status, output = commands.getstatusoutput(message)

        self.pushtotalk.closeport()

# End of File
