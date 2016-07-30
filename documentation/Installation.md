# Installation

```sh
xe1gyq@jessie:~/nuupxe$ ssh root@stn8148.ip.irlp.net
```


```sh
The authenticity of host 'stn8148.ip.irlp.net (138.122.96.139)' can't be established.
ECDSA key fingerprint is fd:e0:28:ae:64:87:e7:28:ae:89:65:c9:76:9d:4d:30.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'stn8148.ip.irlp.net,138.122.96.139' (ECDSA) to the list of known hosts.
root@stn8148.ip.irlp.net's password: 
Linux stn8148 3.2.0-4-686-pae #1 SMP Debian 3.2.78-1 i686

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jul 29 21:17:56 2016 from 38.65.136.138
root@stn8148:~# 
```

```sh
root@stn8148:~# apt-get update
Des:1 http://security.debian.org wheezy/updates Release.gpg [1 554 B]
Des:2 http://security.debian.org wheezy/updates Release [39.0 kB]
Des:3 http://security.debian.org wheezy/updates/main Sources [272 kB]
Des:4 http://security.debian.org wheezy/updates/main i386 Packages [426 kB]
Des:5 http://security.debian.org wheezy/updates/main Translation-en [233 kB]
Des:6 http://cdn.debian.net wheezy Release.gpg [2 373 B]
Des:7 http://cdn.debian.net wheezy Release [191 kB]
Des:8 http://cdn.debian.net wheezy/main Sources [5 993 kB]
Des:9 http://cdn.debian.net wheezy/main i386 Packages [5 857 kB]
Obj http://cdn.debian.net wheezy/main Translation-es
Des:10 http://cdn.debian.net wheezy/main Translation-en [3 846 kB]
Descargados 16.9 MB en 1min. 7seg. (249 kB/s)      
Leyendo lista de paquetes... Hecho
root@stn8148:~# 
```

```sh
root@stn8148:~# apt-get install git
Leyendo lista de paquetes... Hecho
Creando árbol de dependencias       
Leyendo la información de estado... Hecho
Se instalarán los siguientes paquetes extras:
  git-man libcurl3-gnutls liberror-perl
Paquetes sugeridos:
  git-daemon-run git-daemon-sysvinit git-doc git-el git-arch git-cvs git-svn
  git-email git-gui gitk gitweb
Se instalarán los siguientes paquetes NUEVOS:
  git git-man libcurl3-gnutls liberror-perl
0 actualizados, 4 se instalarán, 0 para eliminar y 42 no actualizados.
Necesito descargar 7 976 kB de archivos.
Se utilizarán 15.0 MB de espacio de disco adicional después de esta operación.
¿Desea continuar [S/n]? S
Des:1 http://cdn.debian.net/debian/ wheezy/main libcurl3-gnutls i386 7.26.0-1+wheezy13 [327 kB]
Des:2 http://cdn.debian.net/debian/ wheezy/main liberror-perl all 0.17-1 [23.6 kB]
Des:3 http://cdn.debian.net/debian/ wheezy/main git-man all 1:1.7.10.4-1+wheezy3 [1 075 kB]
Des:4 http://cdn.debian.net/debian/ wheezy/main git i386 1:1.7.10.4-1+wheezy3 [6 551 kB]
Descargados 7 976 kB en 28seg. (278 kB/s)                                      
Seleccionando el paquete libcurl3-gnutls:i386 previamente no seleccionado.
(Leyendo la base de datos ... 30033 ficheros o directorios instalados actualmente.)
Desempaquetando libcurl3-gnutls:i386 (de .../libcurl3-gnutls_7.26.0-1+wheezy13_i386.deb) ...
Seleccionando el paquete liberror-perl previamente no seleccionado.
Desempaquetando liberror-perl (de .../liberror-perl_0.17-1_all.deb) ...
Seleccionando el paquete git-man previamente no seleccionado.
Desempaquetando git-man (de .../git-man_1%3a1.7.10.4-1+wheezy3_all.deb) ...
Seleccionando el paquete git previamente no seleccionado.
Desempaquetando git (de .../git_1%3a1.7.10.4-1+wheezy3_i386.deb) ...
Procesando disparadores para man-db ...
Configurando libcurl3-gnutls:i386 (7.26.0-1+wheezy13) ...
Configurando liberror-perl (0.17-1) ...
Configurando git-man (1:1.7.10.4-1+wheezy3) ...
Configurando git (1:1.7.10.4-1+wheezy3) ...
root@stn8148:~# 
```


```sh
root@stn8148:~# su - repeater
repeater@stn8148:~/$ cd custom/
root@stn8148:~# su - repeater
repeater@stn8148:~/custom$ git clone https://github.com/xe1gyq/nuupxe.git
Cloning into 'nuupxe'...
remote: Counting objects: 3928, done.
remote: Compressing objects: 100% (208/208), done.
remote: Total 3928 (delta 139), reused 0 (delta 0), pack-reused 3719
Receiving objects: 100% (3928/3928), 740.80 KiB | 266 KiB/s, done.
Resolving deltas: 100% (2709/2709), done.
repeater@stn8148:~/custom$ 
```

```sh
repeater@stn8148:~/custom$ cd nuupxe/
repeater@stn8148:~/custom/nuupxe$ ls
configuration  __init__.py  modules	nuupxe.sh  serviceManager.py  TODO
core	       learning     morsefiles	output	   setup
documentation  LICENSE	    nuupxe.py	README.md  SUMMARY.md
repeater@stn8148:~/custom/nuupxe$ 
```

```sh
repeater@stn8148:~/custom/nuupxe$ python nuupxe.py -m identification
Traceback (most recent call last):
  File "nuupxe.py", line 9, in <module>
    from serviceManager import ServiceManager
  File "/home/irlp/custom/nuupxe/serviceManager.py", line 12, in <module>
    from apscheduler.scheduler import Scheduler
ImportError: No module named apscheduler.scheduler
repeater@stn8148:~/custom/nuupxe$ 
```

```sh
repeater@stn8148:~/custom/nuupxe$ exit
logout
root@stn8148:~# ls /home
EchoIRLP  irlp	XE1DGC
root@stn8148:~# cd /home/irlp/custom/nuupxe/
root@stn8148:/home/irlp/custom/nuupxe# 
```

```sh
root@stn8148:/home/irlp/custom/nuupxe# sh setup/systemAptGet.sh
root@stn8148:/home/irlp/custom/nuupxe# sh setup/systemPip.sh
```


```sh
repeater@stn8148:~/custom$ nano custom_decode 
...

# NuupXe Project, Module Mode, Production
if [ "$1" = "P1" ] ; then cd "$CUSTOM"/nuupxe; python nuupxe.py -m weather ; exit 1 ; fi

exit 0 
repeater@stn8148:~/custom$ 
```

```sh
repeater@stn8474:~/custom$ nano custom.crons
#Reporte meteorologico cada 2 horas
00 0,3,6,9,12,15,18,21 * * * (/home/irlp/scripts/decode P4 &>/dev/null 2>&1)
repeater@stn8474:~/custom$ 
```