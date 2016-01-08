#!/bin/bash

../../ttSchweizer.py > out
diff out.expected out
rm out spieler.txt runde-1.txt
