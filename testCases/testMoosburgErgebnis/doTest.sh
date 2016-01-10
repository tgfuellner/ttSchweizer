#!/bin/bash

../../ttSchweizer.py  >/dev/null

# Hängt sich auf
#xmldiff resultRunde6-28.8.xml-expected resultRunde6-28.8.xml

xmllint --c14n resultRunde6-28.8.xml > rr.xml
xmllint --c14n resultRunde6-28.8.xml-expected > expected.xml
diff expected.xml rr.xml


rm runde-7.txt
rm rr.xml expected.xml resultRunde6-28.8.xml
