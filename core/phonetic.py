#!/usr/bin/python

number = {'1': 'uno',    '2': 'dos',   '3': 'tres',
    '4': 'cuatro',  '5': 'cinco',   '6': 'seis',
    '7': 'siete',   '8': 'ocho',    '9': 'nueve',
    '0': 'cero',
    }

phoneticnumber = {'1': 'primero',    '2': 'segundo',   '3': 'tercero',
    '4': 'cuarto',  '5': 'quinto',   '6': 'sexto',
    '7': 'septimo',   '8': 'octavo',    '9': 'noveno',
    '0': 'negativo',
    }

phoneticalphabet = {'A': 'alfa',    'B': 'bravo',   'C': 'charli',
        'D': 'delta',   'E': 'eco', 'F': 'foxtrot',
    'G': 'golf',    'H': 'hotel',   'I': 'india',
    'J': 'yuliet',  'K': 'kilo',    'L': 'lima',
    'M': 'maik',    'N': 'november','O': 'oscar',
    'P': 'papa',    'Q': 'quebec',  'R': 'romeo',
    'S': 'sierra',  'T': 'tango',   'U': 'union',
    'V': 'victor',  'W': 'wiski',   'X': 'exrey',
    'Y': 'yanqui',  'Z': 'zulu',    '@': 'arroba',
    '.': 'punto',   '+': 'positivo','-': 'negativo'
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

if __name__ == '__main__':

    mytest = Phonetic()
    print mytest.decode("hola xe1gyq")
