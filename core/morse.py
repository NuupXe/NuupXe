import sys
import time
import configparser
import subprocess
import pygame

from core.pushtotalk import PushToTalk

CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}


class Morse:
    def __init__(self):
        self.message = ""
        self.oneunit = 0.3
        self.threeunits = 3 * self.oneunit
        self.sevenunits = 7 * self.oneunit
        self.morsefiles = 'morsefiles/'

        conf = configparser.ConfigParser()
        conf.read("configuration/general.config")
        self.morseagent = conf.get("general", "morseagent")

        self.pushtotalk = PushToTalk()

        if self.morseagent == 'pygame':
            pygame.init()

    def verify(self, message):
        for char in message:
            if char.upper() not in CODE and char != ' ':
                raise ValueError(f'Character {char!r} cannot be translated to Morse Code')

    def generate(self, message):
        self.verify(message)
        self.pushtotalk.open_port()

        if self.morseagent == 'pygame':
            for char in message:
                if char == ' ':
                    time.sleep(self.sevenunits)
                else:
                    print(CODE[char.upper()])
                    pygame.mixer.music.load(self.morsefiles + char.upper() + '_morse_code.ogg')
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.01)
                    time.sleep(self.threeunits)

        elif self.morseagent == 'cwpcm':
            # Note: cwpcm pipes to /dev/dsp (OSS) — may not work on ALSA/PulseAudio systems
            cmd = f'echo {message} | /home/irlp/bin/cwpcm -sm -l 007 -p 1000 > /dev/dsp'
            subprocess.run(cmd, shell=True)

        self.pushtotalk.close_port()
