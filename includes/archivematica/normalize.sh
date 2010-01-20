#!/bin/bash
shortfile=`basename "$1"`

if [ -e $1 ];then
  cd /opt/externals/xena/ ; java -jar xena.jar -f $1 -o /tmp/$2 -p plugins/
else
  echo "file does not exist"
fi
