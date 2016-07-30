# Installation

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
Leyendo lista de paquetes... 96%

```

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
root@stn8148:~# su - repeater
repeater@stn8148:~/$ 
```

```sh
root@stn8148:~# su - repeater
repeater@stn8148:~/$ cd custom/
```

