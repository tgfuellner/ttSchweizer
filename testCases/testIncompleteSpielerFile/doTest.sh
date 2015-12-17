#!/bin/bash

../../ttSchweizer.py >out.txt
diff out.txt-expected out.txt
