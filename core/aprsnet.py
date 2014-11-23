import sys, time
from socket import *

class AprsNet(object):

    def __init__(self):

        self.serverHost = '205.233.35.52'
        self.serverPort = 14580
        self.password = '17329'
        self.address = 'XE1GYQ-11>APRS,TCPIP*:'
        self.position = '=2036.92N/10324.72W-'

        self.packet = ''

    def send_packet(self, message):
        sSock = socket(AF_INET, SOCK_STREAM)
        sSock.connect((self.serverHost, self.serverPort))
        sSock.send('user XE1GYQ-11 pass ' + self.password + ' vers "XE1GYQ Cancun Project" \n')
        sSock.send(self.address + self.position + message +'\n')
        print("packet sent: " + time.ctime() )
        sSock.shutdown(0)
        sSock.close()
