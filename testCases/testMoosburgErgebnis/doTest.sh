#!/bin/bash

../../ttSchweizer.py >/dev/null
xmldiff resultRunde6-28.8.xml-expected resultRunde6-28.8.xml

rm runde-7.txt resultRunde6-28.8.xml
