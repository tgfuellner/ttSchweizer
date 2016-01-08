#!/bin/bash

../../ttSchweizer.py > out
diff out.expected out
rm out spieler.txt
