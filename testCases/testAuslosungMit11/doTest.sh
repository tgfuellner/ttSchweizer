#!/bin/bash

../../ttSchweizer.py
diff runde-1.tts-expected <(sed 's/<>.*$/<> /' runde-1.tts)
rm runde-1.tts
