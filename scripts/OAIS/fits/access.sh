#!/bin/bash
NOW=$(date +"%s")
SIP=`echo $@ | sed 's/ /_/g'`

cd /usr/local/OAIS/fits/ ; ./fits.sh -i $1 -o /home/demo/accession/$NOW.log

