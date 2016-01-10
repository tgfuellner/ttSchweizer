#!/bin/bash

../../ttSchweizer.py >/dev/null

# Hängt sich auf
#xmldiff resultRunde6-28.8.xml-expected resultRunde6-28.8.xml

xmllint --c14n --valid  resultRunde6-28.8.xml > rr.xml
xmllint --c14n --valid  resultRunde6-28.8.xml-expected > expected.xml
diff resultRunde6-28.8.xml-expected expected.xml


rm runde-7.txt resultRunde6-28.8.xml
#rm rr.xml expected.xml
