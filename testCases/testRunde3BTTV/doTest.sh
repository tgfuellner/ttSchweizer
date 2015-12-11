#!/bin/bash

F=runde-4.txt

../../ttSchweizer.py > /dev/null
if [ ! -e "$F" ]
then
    echo "$F existiert nicht, sollte aber erstellt werden."
fi
rm $F
