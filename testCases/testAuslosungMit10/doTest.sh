#!/bin/bash

../../ttSchweizer.py
diff runde1.tts-expected <(sed 's/-.*$/- /' runde1.tts)
