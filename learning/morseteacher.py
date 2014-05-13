#!/usr/bin/python

import random
import string
import sys
import time

sys.path.append('../modules')

from morse import Morse
from phonetic import Phonetic
from random import randint
from voicesynthetizer import VoiceSynthetizer

class MorseTeacher(object):

    def __init__(self, voicesynthetizer):
        
        self.morse = Morse()
        self.speaker = voicesynthetizer
        self.phonetic = Phonetic()

    def __del__(self):
        pass

    def message(self, message):
        self.speaker.speechit(message)

    def welcome(self):
        self.message("Modulo de Aprendizaje de Codigo Morse, sugerencias escribir a ")
        self.message(" ".join(self.phonetic.decode('xe1gyq@gmail.com')))

    def randomnumber(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def randomletter(self, n):
        letters = []
        for x in range(0, n):
            letters.append(random.choice(string.ascii_letters))
        return "".join(letters)

    def randomnumberplay(self, help, iterations):
        random = self.randomnumber(iterations)
        self.message("Seccion de Prueba de Numeros Aleatorios")
        for x in str(random):
            if not help:
                self.morse.generate(x)
                self.message("El numero codificado fue, " + x + ", " + " ".join(self.phonetic.decode(x)))
            if help:
                self.message("El numero, " + x + ", " + " ".join(self.phonetic.decode(x)) + "codificado es, ")
                self.morse.generate(x)
            time.sleep(1)

    def randomletterplay(self, help, iterations):
        random = self.randomletter(iterations)
        self.message("Seccion de Prueba de Letras Aleatorias")
        for x in str(random):
            if not help:
                self.morse.generate(x)
                self.message("La letra codificada fue, " + x + ", " + " ".join(self.phonetic.decode(x)))
            if help:
                self.message("La letra, " + x + ", de " + " ".join(self.phonetic.decode(x)) + "codificada es, ")
                self.morse.generate(x)
            time.sleep(1)

    def golearn(self):
        print '[Cancun] Morse Teacher Learning'
        self.welcome()
        self.randomnumberplay(True, 10)
        self.randomnumberplay(False, 10)
        self.message("Hagamos una pausa de 10 segundos")
        time.sleep(10)
        self.randomletterplay(True, 10)
        self.randomletterplay(False, 10)

    def gocompete(self):
        print '[Cancun] Morse Teacher Contest'
        self.message("Concurso Decodificando Texto")
        self.message("Envia tus resultados a " + " ".join(self.phonetic.decode('xe1gyq@gmail.com')))
        self.message("El primer correo con el texto correcto sera ganador de una tarjeta de 200 pesos para Star Bucks")
        self.message("Listo? Comenzamos...")
        file = open('../learning/morsecontest.text')
        for line in file.readlines():
            self.morse.generate(''.join(e for e in line if e.isalnum()))
        return

if __name__ == '__main__':

    mymorse = MorseTeacher()
    mymorse.golearn()
    mymorse.gocompete()
