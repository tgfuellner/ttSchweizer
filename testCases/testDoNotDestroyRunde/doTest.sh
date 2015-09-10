#!/bin/bash

echo foo >runde-1.tts
../../ttSchweizer.py

if ! cmp -s runde-1.tts-expected runde-1.tts; then
    echo "Ein vorhandenes runde-1.tts darf nicht überschrieben werden!"
fi
