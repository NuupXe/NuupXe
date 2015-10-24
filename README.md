# NuupXe Amateur Radio Voice Software Infrastructure

## Production Modules

- Alive
- Aprstt
- Clock.Date
- Clock.Hour
- Identification
- Selfie
- Voice Command
- Weather
- WolframAlpha

## Social Media

- @NuupXe
- #NuupXe

## Groups Required
Add your username to dialout, audio and video groups

## Configurations Files Required

- conf/general.config
- conf/services.config

##

    https://pypi.python.org/pypi/SpeechRecognition/3.1.0
    apt-get install python-pyaudio python3-pyaudio
    

Edison

Make sure your date/time is correct!

    conf/systemPip.sh
    apt-get install python-pygame
    apt-get install mpg123
    apt-get install flac
    
    aplay -Ll
    /etc/asound.conf
     pcm.!default sysdefault:MS
    arecord -f cd -D plughw:1,0 -d 20 test.wav
    aplay -D hw:1,0 test.wav

    wget 'http://www.libsdl.org/release/SDL-1.2.15.tar.gz'
    tar -xf SDL-1.2.15.tar.gz
    cd SDL-1.2.15
    ./configure --prefix=$HOME
    make
    make install

    wget 'http://www.pygame.org/ftp/pygame-1.9.1release.tar.gz'
    tar -xf pygame-1.9.1release.tar.gz
    cd pygame-1.9.1release
    python2.7 setup.py install --prefix=$HOME

## Intel IoT DevKit

Not sure why this is here, anyway! let's keep it!

 $ git clone https://github.com/intel-iot-devkit/mraa.git
 # apt-get install swig cmake
 $ cmake -DBUILDSWIGNODE=OFF ..
 $ make
 # make install
 $ export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/site-packages/

Copyright 2014, Released under Apache License

# End of file
