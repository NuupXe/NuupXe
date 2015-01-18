#!/usr/bin/python

import commands
import pygame
import pygame.camera

from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.voice import Voice

class Camera(object):

    def __init__(self, voicesynthetizer):

        self.mycamera = None
        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.voice = Voice()

        self.voicesynthetizer = voicesynthetizer
        self.picturepygame = 'output/camerapygame.jpg'
        self.picturefswebcam = 'output/camerafswebcam.jpg'
        self.fswebcam = 'fswebcam'
        self.fswebcamarguments = ' -r 1280x1024 -s brightness=65% -s Contrast=50% -s Gamma=100% --jpeg 100 --no-banner '

    def __del__(self):
        pass

    def setup():
        print '[Cancun] Camera Setup'
        pygame.camera.init()
        self.mycamera = pygame.camera.Camera("/dev/video0",(640,480))
        self.mycamera.start()

        self.fswebcamcommand = self.fswebcam + self.fswebcamarguments + self.picturefswebcam

    def capture(self):
        print '[Cancun] Camera Capture'
        image = self.mycamera.get_image()
        pygame.image.save(image, self.picturepygame)
        commands.getstatusoutput(self.fswebcamcommand)

    def post(self):
        print '[Cancun] Camera Post'
        self.pushtotalk.openport()
        self.voicesynthetizer.speechit("Foto Tomada")
        self.pushtotalk.closeport()

# End of file
