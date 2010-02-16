#!/bin/bash
shortfile=`basename "$1"`

if [ -e $1 ];then
  cd /opt/externals/xena/ ; java -jar xena.jar -f $1 -o $2 -p plugins/ >> $2/ingestLogs/normalization.log
else
  echo "file does not exist"
fi
