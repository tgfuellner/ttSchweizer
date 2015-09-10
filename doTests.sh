#!/bin/bash

numberOdTests=0

for t in testCases/test*
do
 echo "******** $t"
 (cd $t; ./doTest.sh)
 numberOdTests=$[numberOdTests + 1]
done

echo "==================================="
echo "$numberOdTests Tests executed"
