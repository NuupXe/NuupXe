#!/usr/bin/python

import logging

from core.wolfram import Wolfram

class Poc(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.wolfram = Wolfram()

    def setup(self):

        pass

    def report(self):

        logging.info('Poc Report')
        self.setup()
        self.voicesynthetizer.setlanguage("english")
        question = 'What is the capital of USA'
        self.voicesynthetizer.speechit(question)
        answer = self.wolfram.question(question)       
        self.voicesynthetizer.speechit(answer)
        self.voicesynthetizer.setlanguage("spanish")


# End of File
