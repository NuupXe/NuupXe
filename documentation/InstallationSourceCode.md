# Source Code

```sh
root@stn8148:~# su - repeater
repeater@stn8148:~/$ cd custom/
root@stn8148:~# su - repeater
```

```sh
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
configuration  __init__.py  modules    nuupxe.sh  serviceManager.py  TODO
core           learning     morsefiles    output       setup
documentation  LICENSE        nuupxe.py    README.md  SUMMARY.md
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



