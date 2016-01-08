#!/bin/bash

../../ttSchweizer.py >/dev/null
diff resultRunde6-28.8.xml-expected resultRunde6-28.8.xml

rm runde-7.txt resultRunde6-28.8.xml
