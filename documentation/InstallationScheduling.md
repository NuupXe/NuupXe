# Scheduling

```sh
repeater@stn8148:~/custom$ nano custom_decode 
```

```sh
...
...

# NuupXe Project, Module Mode, Production
if [ "$1" = "P1" ] ; then cd "$CUSTOM"/nuupxe; python nuupxe.py -m identification ; exit 1 ; fi
if [ "$1" = "P2" ] ; then cd "$CUSTOM"/nuupxe; python nuupxe.py -m weather ; exit 1 ; fi

# NuupXe  Project, Module Mode, Experimental
if [[ "$1" == PS* ]] ; then cd "$CUSTOM"/nuupxe; python nuupxe.py -d $1 ; exit 1 ; fi

exit 0 
```

```sh
repeater@stn8148:~/custom$ nano custom.crons
```

```sh
...
...
# Identificacion
05 0,3,6,9,12,15,18,21 * * * (/home/irlp/scripts/decode P1 &>/dev/null 2>&1)

# Reporte meteorologico cada 3 horas
30 0,3,6,9,12,15,18,21 * * * (/home/irlp/scripts/decode P2 &>/dev/null 2>&1)
```

