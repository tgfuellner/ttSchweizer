#!/bin/bash

echo "foo <> bar ! " >runde-1.txt
../../ttSchweizer.py >out

if ! cmp -s runde-1.tts-expected runde-1.txt; then
    echo "Ein vorhandenes runde-1.txt darf nicht überschrieben werden!"
fi

diff out out-expected
rm out
