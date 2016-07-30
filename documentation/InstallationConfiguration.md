# Configuration

```sh
repeater@stn8148:~/custom$ nano custom_decode 
...

# NuupXe Project, Module Mode, Production
if [ "$1" = "P1" ] ; then cd "$CUSTOM"/nuupxe; python nuupxe.py -m weather ; exit 1 ; fi

exit 0 
repeater@stn8148:~/custom$ 
```

```
repeater@stn8474:~/custom/nuupxe$ ls configuration/
aprstt.config  general.config	stations.config     voicerss.ak
custom_decode  services.config	voicemailer.config  voicerss.mk
repeater@stn8474:~/custom/nuupxe$ 
```
