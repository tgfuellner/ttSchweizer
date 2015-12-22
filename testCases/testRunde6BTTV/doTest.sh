#!/bin/bash

F=runde-7.txt

../../ttSchweizer.py >out.txt

#if [ -e "$F" ]
#then
#    echo "$F sollte nicht mehr erzeugt werden, das Turnier ist beendet"
#fi

diff out.txt out.txt-expected

rm $F out.txt
