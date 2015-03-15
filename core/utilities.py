#!/usr/bin/python

import uuid

def Randomizer(length=2):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace('-',"")
    return random[0:length]

def BytesToHuman(n):
    """
    >>> bytes2human(10000)
    '9.8 KB'
    >>> bytes2human(100001221)
    '95.4 MB'
    """
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)

# End of File
