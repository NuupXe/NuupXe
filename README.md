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

Edison

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
