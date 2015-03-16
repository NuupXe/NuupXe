#!/usr/bin/python
# -*- coding: latin-1 -*-
import commands
import ConfigParser
import logging
import serial
import subprocess
import sys
import time

from core.irlp import Irlp

class PushToTalk(object):

    def __init__(self):
        self.portdefault = None
        self.port = None

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.portdefault = self.conf.get("general", "serialport")

        self.irlp = Irlp()

    def __del__(self):
        if (self.port):
            self.port.close()

    def openport(self):

        logging.info('Push To Talk Open Port')
        try:
            self.irlp.busy()
            self.irlp.forceptt()
            self.port = serial.Serial(self.portdefault, baudrate=115200, timeout=3.0)
            self.port.write("\r\nLet's push the PTT")
            self.port.write("Confirm PTT")
            self.port.flush()
        except:
            pass

    def closeport(self):

        logging.info('Push To Talk Open Port')
        try:
            self.irlp.forceunptt()
            self.port.close()
        except:
            pass

    def message(self, msg):

        logging.info('Push To Talk Message')
        self.openport()
        proc = subprocess.call(msg)
        logging.info(msg)
        self.closeport()

# End of File
