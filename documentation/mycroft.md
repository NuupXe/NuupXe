```sh
pymelab@workstation:~$ git clone https://github.com/MycroftAI/mycroft-core.git
Clonar en «mycroft-core»...
remote: Counting objects: 5086, done.
remote: Total 5086 (delta 0), reused 0 (delta 0), pack-reused 5085
Receiving objects: 100% (5086/5086), 74.37 MiB | 596.00 KiB/s, done.
Resolving deltas: 100% (2888/2888), done.
Comprobando la conectividad… hecho.
pymelab@workstation:~$ 
```

```sh
pymelab@workstation:~/mycroft-core$ ./build_host_setup_debian.sh 
```

```sh
pymelab@workstation:~/mycroft-core$ ./dev_setup.sh 
```

# PocketSphynx

```
sudo apt-get install -qq python python-dev python-pip build-essential swig libpulse-dev
```

```sh
sudo pip install pocketsphinx
```

```sh
pymelab@workstation:~/speech_recognition/examples$ sudo pip install pyaudio --upgrade
```

#PyuAudio

```sh
sudo apt-get remove python-pyaudio
sudo apt-get -f install
sudo apt-get autoremove
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pyaudio
```
