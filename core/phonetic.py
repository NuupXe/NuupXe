#!/usr/bin/python

number = {'1': 'Uno',    '2': 'Dos',   '3': 'Tres',
    '4': 'Cuatro',  '5': 'Cinco',   '6': 'Seis',
    '7': 'Siete',   '8': 'Ocho',    '9': 'Nueve',
    '0': 'Cero',
    }

phoneticnumber = {'1': 'Primero',    '2': 'Segundo',   '3': 'Tercero',
    '4': 'Cuarto',  '5': 'Quinto',   '6': 'Sexto',
    '7': 'Septimo',   '8': 'Octavo',    '9': 'Noveno',
    '0': 'Negativo',
    }

phoneticalphabet = {'A': 'Alpha',     'B': 'Bravo',   'C': 'Charlie',
    'D': 'Delta',   'E': 'Echo',      'F': 'Foxtrot',
    'G': 'Golf',    'H': 'Hotel',     'I': 'India',
    'J': 'Juliet',  'K': 'Kilo',      'L': 'Lima',
    'M': 'Mike',    'N': 'November',  'O': 'Oscar',
    'P': 'Papa',    'Q': 'Quebec',    'R': 'Romeo',
    'S': 'Sierra',  'T': 'Tango',     'U': 'Uniform',
    'V': 'Victor',  'W': 'Whiskey',   'X': 'Xray',
    'Y': 'Yankee',  'Z': 'Zulu',      '@': 'Arroba',
    '.': 'Punto',   '+': 'Positivo',  '-': 'Negativo',
    '#': 'Gato',    '*': 'Asterisco', '/': 'Diagonal'
    }

class Phonetic(object):

    def __init__(self):
        self.temp = []

    def decodenumber(self, character):
        return number[character.upper()]

    def decodephoneticnumber(self, character):
        return phoneticnumber[character.upper()]

    def decodephoneticalphabet(self, character):
        return phoneticalphabet[character.upper()]

    def decode(self, characters):
        self.list = []
        characters = characters.replace(" ", "")
        for character in characters:
            if character.isdigit():
                self.list.append(self.decodephoneticnumber(character))
            else:
                self.list.append(self.decodephoneticalphabet(character.upper()))
        return self.list

# End of File
