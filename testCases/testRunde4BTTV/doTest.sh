#!/bin/bash

F=runde-5.tts

../../ttSchweizer.py
if [ ! -e "$F" ]
then
    echo "$F existiert nicht, sollte aber erstellt werden."
fi
rm $F
