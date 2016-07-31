# Modules


```sh
xe1gyq@jessie:~/nuupxe$ sudo pip install colorclass
[sudo] password for xe1gyq: 
Collecting colorclass
  Downloading colorclass-2.2.0.tar.gz
Building wheels for collected packages: colorclass
  Running setup.py bdist_wheel for colorclass ... done
  Stored in directory: /root/.cache/pip/wheels/a8/d1/a2/8f01754e697c17034f2dc2ca4db6f984194b778872a44ff4bf
Successfully built colorclass
Installing collected packages: colorclass
Successfully installed colorclass-2.2.0
xe1gyq@jessie:~/nuupxe$ python
Python 2.7.9 (default, Mar  1 2015, 18:22:53) 
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from colorclass import Color
>>> 
>>> print(Color(
...     '{autored}[{/red}{autoyellow}+{/yellow}{autored}]{/red} {autocyan}Cargando plugins...{/cyan}'))
[+] Cargando plugins...
```