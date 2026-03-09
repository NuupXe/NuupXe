#!/usr/bin/python

import logging

from core.alive import alive
from core.voicerecognition import VoiceRecognition
from core.wolfram import Wolfram

class WolframAlpha(object):

    def __init__(self, voicesynthesizer):

        self.modulename = 'WolframAlpha'
        self.voicesynthesizer = voicesynthesizer
        self.voicerecognition = VoiceRecognition(self.voicesynthesizer)
        self.wolfram = Wolfram()

    def setup(self):
        logging.info('Wolfram Alpha Setup')
        self.voicerecognition.languageset('english')
        self.voicesynthesizer.set_language("english")

    def cleanup(self):
        logging.info('Wolfram Alpha Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthesizer.set_language("spanish")

    def ask(self):
        logging.info('Wolfram Alpha Ask')
        self.setup()
        self.voicesynthesizer.speech_it('Yes! What is your question for Wolfram Alpha?')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        questionmessage = 'Question? ' + question
        logging.info(questionmessage)
        self.voicesynthesizer.speech_it(question)
        answer = self.wolfram.question(question)
        if answer is not None:
            self.voicesynthesizer.speech_it(answer)
            answermessage = 'Answer? ' + answer
            logging.info(answermessage)
        else:
            answermessage = 'Answer? Sorry! Something went wrong!'
            self.voicesynthesizer.speech_it(answermessage)
        self.cleanup()
        alive(modulename=self.modulename, modulemessage=questionmessage + ' ' + answermessage)

# End of File
