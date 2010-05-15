#!/bin/bash
shortfile=`basename "$1"`

if [ -e $1 ];then
  cd /opt/externals/fits/ ; ./fits.sh -i $1 -o /home/demo/ingestLogs/$2/FITS-$shortfile.xml
else
  echo "file does not exist"
fi

