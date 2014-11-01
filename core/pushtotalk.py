import commands
import ConfigParser
import serial
import sys
import time

class PushToTalk(object):

    def __init__(self):
        self.portdefault = None
        self.port = None

        self.conf = ConfigParser.ConfigParser()
        self.path = "configuration/general.config"
        self.conf.read(self.path)
        self.portdefault = self.conf.get("general", "serialport")

    def __del__(self):
        if (self.port):
            self.port.close()

    def openport(self):
        try:
            commands.getstatusoutput("/home/irlp/bin/coscheck")
            commands.getstatusoutput("/home/irlp/scripts/off")
            commands.getstatusoutput("/home/irlp/bin/forcekey")
            self.port = serial.Serial(self.portdefault, baudrate=115200, timeout=3.0)
            self.port.write("\r\nLet's push the PTT")
            self.port.write("Confirm PTT")
            self.port.flush()
        except:
            pass

    def closeport(self):
        try:
            commands.getstatusoutput("/home/irlp/bin/forceunkey")
            self.port.close()
        except:
            pass

    def message(self, msg):

        self.openport()
        status, output = commands.getstatusoutput(msg)
        self.closeport()

if __name__ == "__main__":
    mytest = PushToTalk()
