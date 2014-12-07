#!/bin/sh

stop() {
    pid=`ps -ef | grep 'cancun.py' | awk '{ print $2 }'`
    kill $pid
    echo "Cancun Project Killed!"
    test -f /tmp/cancun.pid && rm -f /tmp/cancun.pid
    /home/irlp/bin/forceunkey
}

case "$1" in
  stop)
    stop
    ;;
  *)
    echo "Usage: cancun.sh stop"
    exit 1
esac

