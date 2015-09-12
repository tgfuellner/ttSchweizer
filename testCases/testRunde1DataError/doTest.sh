#!/bin/bash

../../ttSchweizer.py >out
diff out-expected out
