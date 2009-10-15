#!/bin/bash
shortfile=`basename "$1"`

if [ -e $1 ];then
  cd /usr/local/OAIS/fits/ ; ./fits.sh -i $1 -o /home/demo/accessionrecords/$2/$shortfile.log
else
  echo "file does not exist"
fi

