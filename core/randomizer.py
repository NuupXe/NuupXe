#!/usr/bin/python

import uuid

def randomize(length=10):
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace('-',"")
    return random[0:length]

# End of File
