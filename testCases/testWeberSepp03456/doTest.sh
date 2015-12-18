#!/bin/bash

F=runde-3.txt

../../ttSchweizer.py >out.txt
if [ -e "$F" ]
then
    echo "$F sollte nicht erstellt werden."
fi

diff out.txt out.txt-expected

rm out.txt
