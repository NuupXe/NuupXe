#!/usr/bin/python

import subprocess
import logging
import time
import pyaudio
import math
import struct
import wave

from core.irlp import Irlp
from core.pushtotalk import PushToTalk
from core.speechrecognition import SpeechRecognition
from core.voice import Voice

class VoiceRecognition(object):

    def __init__(self, voicesynthetizer):

        self.output = ""
        self.agent = "pyaudio"
        self.language = 'spanish'
        self.audiofilewav = "output/voicerecognition.wav"
        self.audiofileflac = "output/voicrecognition.flac"
        self.voicesynthetizer = voicesynthetizer

        self.irlp = Irlp()
        self.pushtotalk = PushToTalk()
        self.speechrecognition = SpeechRecognition()
        self.voice = Voice()

        self.voice.filenameset(self.audiofilewav)

    def __del__(self):
        pass
        command = "rm " + self.audiofilewav
        subprocess.call(command, shell=True)
        command = "rm " + self.audiofileflac
        subprocess.call(command, shell=True)

    def languageset(self, language):

        logging.info('Voice Recognition Language Set')

        self.language = language
        self.speechrecognition.languageset(self.language)

    def filegetname(self):

        logging.info('Voice Recogntion File Get Name')

        return self.audiofilewav

    def rms(self, frame):
        count = len(frame)/2
        format = "%dh" % count
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0
        for sample in shorts:
            sum_squares += sample*sample
        return math.sqrt(sum_squares / count)

    def record(self):

        logging.info('Voice Recognition Record')

        if self.agent == 'nexiwave':
            command = 'arecord -vv -f cd -d 5 ' + self.audiofilewav
            subprocess.call(command, shell=True)
        elif self.agent == 'google':
            self.voice.record()
            command = "flac -f -o " + self.audiofileflac + " --channels=1 --sample-rate=48000 " + self.audiofilewav
            subprocess.call(command, shell=True)
        elif self.agent == "pyaudio":
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 1024
            THRESHOLD = 500
            SILENCE_DURATION = 4

            audio = pyaudio.PyAudio()

            stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

            print("Recording...")
            frames = []
            silent_chunks = 0
            while True:
                data = stream.read(CHUNK)
                frames.append(data)

                audio_level = self.rms(data)
                if audio_level < THRESHOLD:
                    silent_chunks += 1
                else:
                    silent_chunks = 0

                if silent_chunks >= RATE / CHUNK * SILENCE_DURATION:
                    break
            print("Finished recording")
            stream.stop_stream()
            stream.close()
            audio.terminate()

            with wave.open(self.audiofilewav, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))

    def recognize(self, speech):

        logging.info('Voice Recognition Decode')

        if speech == 'True':
            self.pushtotalk.openport()
            self.voice.play()
            self.pushtotalk.closeport()

        if self.agent == 'nexiwave':
            self.output = self.speechrecognition.openai(self.audiofilewav)
        elif self.agent == 'pyaudio':
            self.output = self.speechrecognition.openai(self.audiofilewav)
        elif self.agent == 'google':
            self.output = self.speechrecognition.google(self.audiofileflac)

        return self.output

# End of File
