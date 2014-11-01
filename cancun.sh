#!/bin/sh

start() {
    python cancun.py -s &
    echo "Cancun Project | Started in Scheduler mode..."
}
 
stop() {
    pid=`ps -ef | grep 'cancun.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Cancun Project | Scheduler mode killed!"
    rm -f /tmp/cancun.pid
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: cancun.sh {start|stop|restart}"
    exit 1
esac
exit 0
