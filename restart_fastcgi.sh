#!/bin/sh
echo "Resting......"

PROJDIR="/zzdata/gamecard"
PIDFILE="/tmp/gamecard.pid"
SOCKET="/tmp/gamecard.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

/usr/bin/python $PROJDIR/manage.py runfcgi method=prefork socket=$SOCKET pidfile=$PIDFILE
/bin/chown www:www $SOCKET
