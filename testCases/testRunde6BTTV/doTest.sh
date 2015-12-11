#!/bin/bash

F=runde-7.txt

../../ttSchweizer.py
if [ -e "$F" ]
then
    echo "$F sollte nicht mehr erzeugt werden, das Turnier ist beendet"
fi
