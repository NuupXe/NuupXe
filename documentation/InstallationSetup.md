# Setup

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



