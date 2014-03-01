import commands
import serial
import sys
import time

class PushToTalk():

	def __init__(self):
		self.portdefault = "/dev/ttyS0"

	def openport(self):
		try:
			self.port = serial.Serial(self.portdefault, baudrate=115200, timeout=3.0)
			self.port.write("\r\nLet's push the PTT")
			rcv = self.port.read(10)
			self.port.write("\r\nWere we successful?" + repr(rcv))
			time.sleep(3)
		except:
			pass

        def closeport(self):
		try:
			self.port.close()
		except:
			pass

if __name__ == "__main__":

	mytest = PushToTalk()
