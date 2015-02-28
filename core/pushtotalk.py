import commands
import ConfigParser
import serial
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
        try:
            self.irlp.forceunptt()
            self.port.close()
        except:
            pass

    def message(self, msg):
        self.openport()
        status, output = commands.getstatusoutput(msg)
        self.closeport()

# End of File
