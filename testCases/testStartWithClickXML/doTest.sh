#!/bin/bash

../../ttSchweizer.py >out.txt
diff spieler.tts-expected spieler.tts
diff out.txt-expected out.txt
rm spieler.tts runde-1.tts out.txt
