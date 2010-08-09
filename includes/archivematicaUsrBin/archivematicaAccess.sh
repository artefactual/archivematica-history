#!/bin/bash
NOW=`date +%s`
shortfile=`basename "$1"`

if [ -e $1 ];then
  cd /opt/externals/fits/ ; ./fits.sh -i $1 -o /home/demo/ingestLogs/$2/$shortfile.log
else
  echo "$1 was had by the viri checker"
fi
