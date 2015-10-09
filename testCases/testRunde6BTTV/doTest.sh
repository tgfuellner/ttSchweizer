#!/bin/bash

F=runde-7.tts

../../ttSchweizer.py
if [ -e "$F" ]
then
    echo "$F sollte nicht mehr erzeugt werden, das Turnier ist beendet"
fi
