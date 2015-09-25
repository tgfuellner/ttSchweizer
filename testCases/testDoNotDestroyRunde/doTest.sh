#!/bin/bash

echo "foo <> bar ! " >runde-1.tts
../../ttSchweizer.py >out

if ! cmp -s runde-1.tts-expected runde-1.tts; then
    echo "Ein vorhandenes runde-1.tts darf nicht überschrieben werden!"
fi

diff out out-expected
rm out
