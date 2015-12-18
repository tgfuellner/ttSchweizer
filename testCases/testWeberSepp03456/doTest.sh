#!/bin/bash

F=runde-3.txt

../../ttSchweizer.py >/dev/null
if [ ! -e "$F" ]
then
    echo "$F existiert nicht, sollte aber erstellt werden."
fi

echo "Bin mir nicht klar was getestet werden soll"
#if grep -q "Michi <> Mourad" $F
#then
#    echo "Die Begegnung Michi <> Mourad darf nicht in $F vorhanden sein"
#fi

rm $F
