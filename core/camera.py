#!/usr/bin/python

import commands
import pygame
import pygame.camera

class Camera(object):

    def __init__(self, voicesynthetizer):

        self.mycamera = None

        self.voicesynthetizer = voicesynthetizer
        self.picturepygame = 'output/camerapygame.jpg'
        self.picturefswebcam = 'output/camerafswebcam.jpg'
        self.fswebcam = 'fswebcam'
        self.fswebcamarguments = ' -r 1280x1024 -s brightness=65% -s Contrast=50% -s Gamma=100% --jpeg 100 --no-banner '

    def __del__(self):
        pass

    def setup(self):
        print '[Cancun] Camera Setup'
        pygame.camera.init()
        self.mycamera = pygame.camera.Camera("/dev/video0",(640,480))
        self.mycamera.start()

        self.fswebcamcommand = self.fswebcam + self.fswebcamarguments + self.picturefswebcam

    def capture(self):
        print '[Cancun] Camera Capture'
        image = self.mycamera.get_image()
        pygame.image.save(image, self.picturepygame)
        self.mycamera.stop()
        status, output = commands.getstatusoutput(self.fswebcamcommand)

    def post(self):
        print '[Cancun] Camera Post'
        self.voicesynthetizer.speechit("Foto Tomada")

    def execute(self):
        self.setup()
        self.capture()
        self.post()

# End of file
