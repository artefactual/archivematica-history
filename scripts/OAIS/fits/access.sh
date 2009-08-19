#!/bin/bash
NOW=`date +%s`
SIP=`echo $@ | sed 's/ /_/g'`
shortfile=`basename "$1"`


mkdir /home/demo/accessionrecords/$NOW
cd /usr/local/OAIS/fits/ ; ./fits.sh -i $1 -o /home/demo/accessionrecords/$NOW/$shortfile.log

