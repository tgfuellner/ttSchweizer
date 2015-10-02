#!/bin/bash

F=runde-4.tts

../../ttSchweizer.py
if [ ! -e "$F" ]
then
    echo "$F existiert nicht, sollte aber erstellt werden."
fi
rm $F
