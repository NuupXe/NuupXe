#!/usr/bin/python

NUMBER = {
    '1': 'Uno',    '2': 'Dos',    '3': 'Tres',
    '4': 'Cuatro', '5': 'Cinco',  '6': 'Seis',
    '7': 'Siete',  '8': 'Ocho',   '9': 'Nueve',
    '0': 'Cero',
}

PHONETIC_NUMBER = {
    '1': 'Primero',  '2': 'Segundo', '3': 'Tercero',
    '4': 'Cuarto',   '5': 'Quinto',  '6': 'Sexto',
    '7': 'Septimo',  '8': 'Octavo',  '9': 'Noveno',
    '0': 'Negativo',
}

PHONETIC_ALPHABET = {
    'A': 'Alfa',     'B': 'Bravo',    'C': 'Charlie',
    'D': 'Delta',    'E': 'Eko',      'F': 'Foxtrot',
    'G': 'Golf',     'H': 'Hotel',    'I': 'India',
    'J': 'Yuliet',   'K': 'Kilo',     'L': 'Lima',
    'M': 'Maik',     'N': 'November', 'O': 'Oscar',
    'P': 'Papa',     'Q': 'Quebec',   'R': 'Romeo',
    'S': 'Sierra',   'T': 'Tango',    'U': 'Uniforme',
    'V': 'Victor',   'W': 'Whiskey',  'X': 'Eksrey',
    'Y': 'Yankee',   'Z': 'Zulu',     '@': 'Arroba',
    '.': 'Punto',    '+': 'Positivo', '-': 'Negativo',
    '#': 'Gato',     '*': 'Asterisco','/' : 'Diagonal',
}


class Phonetic(object):

    def decodenumber(self, character):
        return NUMBER[character.upper()]

    def decodephoneticnumber(self, character):
        return PHONETIC_NUMBER[character.upper()]

    def decodephoneticalphabet(self, character):
        return PHONETIC_ALPHABET[character.upper()]

    def decode(self, characters):
        result = []
        characters = characters.replace(" ", "")
        for character in characters:
            if character.isdigit():
                result.append(self.decodephoneticnumber(character))
            else:
                result.append(self.decodephoneticalphabet(character.upper()))
        return result

# End of File
