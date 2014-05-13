import commands
import ConfigParser
import serial
import sys
import time

class PushToTalk(object):

    def __init__(self):
        self.portdefault = None

        self.conf = ConfigParser.ConfigParser()
        self.path = "../configuration/general.configuration"
        self.conf.read(self.path)
        self.portdefault = self.conf.get("general", "serialport")

    def __del__(self):
        if (self.port):
            self.port.close()

    def openport(self):
        try:
            self.port = serial.Serial(self.portdefault, baudrate=115200, timeout=3.0)
            self.port.write("\r\nLet's push the PTT")
            self.port.write("Confirm PTT")
        except:
            pass

    def closeport(self):
        self.port.close()

    def message(self, msg):
        try:
            self.openport()
            status, output = commands.getstatusoutput(msg)
            self.closeport()
        except:
            self.closeport()

if __name__ == "__main__":
    mytest = PushToTalk()
