#!/bin/bash
shortfile=`basename "$1"`

cd /usr/local/OAIS/fits/ ; ./fits.sh -i $1 -o /home/demo/accessionrecords/$2/$shortfile.log
