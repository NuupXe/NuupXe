#!/usr/bin/python
# -*- coding: latin-1 -*-

import subprocess
import configparser
import logging
import serial
from pydub import AudioSegment
from pydub.playback import play
from core.irlp import Irlp

class PushToTalk(object):

    def __init__(self):
        self.portdefault = None
        self.port = None

        self.conf = configparser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.portdefault = self.conf.get("general", "serialport")

        self.irlp = Irlp()

    def __del__(self):
        if self.port:
            self.port.close()

    def open_port(self):
        logging.info('Push To Talk Open Port')
        try:
            self.irlp.busy()
            self.irlp.forceptt()
            self.port = serial.Serial(self.portdefault, baudrate=115200, timeout=3.0)
            self.port.write("\r\nLet's push the PTT")
            self.port.write("Confirm PTT")
            self.port.flush()
        except Exception as e:
            logging.error(f'Error opening port: {e}')

    def close_port(self):
        logging.info('Push To Talk Close Port')
        try:
            self.irlp.forceunptt()
            self.port.close()
        except Exception as e:
            logging.error(f'Error closing port: {e}')

    def play_audio(self, audio_path):
        audio = AudioSegment.from_file(audio_path)
        play(audio)

    def message(self, resource_type, msg):
        logging.info('Push To Talk Message')
        self.open_port()
        print(msg)
        if resource_type == "text":
            subprocess.call(msg, shell=True)
        elif resource_type == "audio":
            self.play_audio(msg)
        logging.info(msg)
        self.close_port()
