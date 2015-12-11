#!/bin/bash

../../ttSchweizer.py
diff runde-1.tts-expected <(sed 's/<>.*$/<> /' runde-1.txt)
rm runde-1.txt
