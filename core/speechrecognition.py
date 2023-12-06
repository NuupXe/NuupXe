#!/usr/bin/python

import logging
import sys, os, json, urllib, time
import subprocess
import configparser
import requests

from openai import OpenAI

class SpeechRecognition(object):

    def __init__(self):

        self.language = 'es-MX'
        self.flaccont = None
        self.conf = configparser.ConfigParser()
        self.path = "configuration/services.config"
        self.conf.read(self.path)

    def languageset(self, language):

        logging.info('SpeechRecognition LanguageSet %s', language)
        if language == 'english':
            self.language = 'en-US'
        elif language == 'spanish':
            self.language = 'es-MX'

    def googleX(self, audiofile):

        self.key = self.conf.get("google", "api_key")
        #command = "curl -X POST --data-binary @'" + audiofile + "' --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=es-es&key=" + self.key +"'"
        command = "curl -X POST --data-binary @'" + audiofile + "' --header 'Content-Type: audio/x-flac; rate=48000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=" + self.language + "&key=" + self.key +"'"
        status, output = commands.getstatusoutput(command)
        return output

    def audioread(self, audiofile):

        logging.info('SpeechRecognition Audio Read')
        f = open(audiofile, 'rb')
        self.flaccont = f.read()
        f.close()

    def google(self, audiofile):

        logging.info('SpeechRecognition Google')
        self.audioread(audiofile)
        self.key = self.conf.get("google", "api_key")
        speechurl = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=' + self.language + '&key=' + self.key
        hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",
               'Content-type': 'audio/x-flac; rate=48000'}
        req = urllib2.Request(speechurl, data=self.flaccont, headers=hrs)
        logging.info("Sending request to Google TTS")
        p = urllib2.urlopen(req)
        response = p.read()
        response = response.split('\n', 1)[1]
        result = json.loads(response)['result'][0]['alternative'][0]['transcript']
        logging.info('Result: %s', result)
        return result

    def nexiwave(self, audiofile):

        self.username = self.conf.get("nexiwave", "username")
        self.password = self.conf.get("nexiwave", "password")
        filename = audiofile
        """Transcribe an audio file using Nexiwave"""
        url = 'https://api.nexiwave.com/SpeechIndexing/file/storage/' + self.username +'/recording/?authData.passwd=' + self.password + '&auto-redirect=true&response=application/json'
        sys.stderr.write("Send audio for transcript with " + url + "\n")
        r = requests.post(url, files={'mediaFileData': open(filename,'rb')})
        data = r.json()
        transcript = data['text']
        print("Transcript for " + filename + " = " + transcript)
        return transcript

    def openai(self, audiofile):

        logging.info('SpeechRecognition OpenAI')
        services = configparser.ConfigParser()
        path = "configuration/services.config"
        services.read(path)
        api_key = services.get("openai", "api_key")

        client = OpenAI(api_key=api_key)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(audiofile, "rb"),
            language="es"
        )

        return transcript.text

# End of File
