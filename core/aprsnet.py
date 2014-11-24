import sys, time
from socket import *

class AprsNet(object):

    def __init__(self):

        self.serverHost = '205.233.35.52'
        self.serverPort = 14580
        self.password = '17329'
        self.address = 'XE1GYQ-12'
        self.path = '>APRS,TCPIP*:'
        self.position = '=2036.92N/10324.72W-'

        self.packet = ''

    def address_set(self, address):
        self.address = address

    def position_set(self, position):
        self.position = position

    def send_packet(self, message):
        sSock = socket(AF_INET, SOCK_STREAM)
        sSock.connect((self.serverHost, self.serverPort))
        sSock.send('user XE1GYQ pass ' + self.password + ' vers "XE1GYQ Cancun Project" \n')
        sSock.send(self.address + self.path + self.position + message +'\n')
        print("packet sent: " + time.ctime() )
        sSock.shutdown(0)
        sSock.close()

    def send_packet_raw(self, message):
        sSock = socket(AF_INET, SOCK_STREAM)
        sSock.connect((self.serverHost, self.serverPort))
        sSock.send('user XE1GYQ pass ' + self.password + ' vers "XE1GYQ Cancun Project" \n')
        sSock.send(message +'\n')
        print("packet sent: " + time.ctime() )
        sSock.shutdown(0)
        sSock.close()
