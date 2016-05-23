# NuupXe Amateur Radio Voice Software Infrastructure

https://drive.google.com/file/d/0B6h7kxp-oIy8bUdLTjZSZVJqMG8a/view?usp=sharing

## ToDo

- Add Wunderground to Weather Module
- http://forecast.io/#/f/20.6682,-103.4626

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
- Telegram NuupXeBot

## Groups Required
Add your username to dialout, audio and video groups

## Configurations Files Required

- conf/general.config
- conf/services.config

## To Implement
    
- https://pypi.python.org/pypi/SpeechRecognition/3.1.0
  - apt-get install python-pyaudio python3-pyaudio
- dig https://pypi.python.org/pypi/dig/0.1.10
  - manual install requests 2.8.1
  - manuel install futures 3.0.3
- Telegram Bot
    

Edison

Make sure your date/time is correct!

    conf/systemPip.sh
    apt-get install python-pygame
    apt-get install mpg123
    apt-get install flac
    
    root@ubilinux:/home/edison# apt-get install git libffi-dev libssl-dev
    root@ubilinux:/home/edison# apt-get install python-dev libxml2-dev libxslt1-dev
    root@ubilinux:/home/edison# pip install requests[security] scrapy
    root@ubilinux:/home/edison# pip install pyopenssl ndg-httpsclient pyasn1 scrapy

    
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

http://www.sqlalchemy.org/features.html
http://henrywconklin.github.io/projects/2015/08/17/oliver-twitter.html

# End of file

