#!/bin/sh

stop() {
    pid=`ps -ef | grep 'nuupxe.py' | awk '{ print $2 }'`
    kill $pid
    echo "NuupXe Project Killed!"
    test -f /tmp/nuupxe.pid && rm -f /tmp/nuupxe.pid
    /home/irlp/bin/forceunkey
}

case "$1" in
  stop)
    stop
    ;;
  *)
    echo "Usage: nuupxe.sh stop"
    exit 1
esac

