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
        self.message = ""
        self.oneunit = 0.5
        self.threeunits = 3 * self.oneunit
        self.sevenunits = 7 * self.oneunit
        self.morsefiles = 'morsefiles/'

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.morseagent = self.conf.get("general", "morseagent")

        if self.morseagent is 'pygame':
            pygame.init()

        self.pushtotalk = PushToTalk()

    def verify(self, string):
        keys = code.keys()
        for char in string:
            if char.upper() not in keys and char != ' ':
                sys.exit('Error the character ' + char + ' cannot be translated to Morse Code')

    def generate(self, message):

        self.pushtotalk.openport()
        self.message = message

        if self.morseagent is 'pygame':

            self.verify(message)
            for char in self.message:
                if char == ' ':
                    print ' '*7,
                    time.sleep(self.sevenunits)
                else:
                    print code[char.upper()],
                    print
                    pygame.mixer.music.load(self.morsefiles + char.upper() + '_morse_code.ogg')
                    pygame.mixer.music.play()
                    time.sleep(self.threeunits)

        else:

            self.message = 'echo ' + self.message + ' | ' + self.morseagent + ' -sf -l 007 -p 1000 > /dev/dsp'
            status, output = commands.getstatusoutput(self.message)

        self.pushtotalk.closeport()

if __name__ == '__main__':

    mytest = Morse()
    mytest.generate("abc")
