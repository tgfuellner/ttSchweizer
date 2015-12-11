#!/bin/bash

../../ttSchweizer.py >out.txt
diff spieler.tts-expected spieler.txt
diff out.txt-expected out.txt
rm spieler.txt runde-1.txt out.txt
