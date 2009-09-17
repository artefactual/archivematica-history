#!/bin/bash

find ~/quarantine/* -amin +2 -print| while read FILE
do
  #move file to quarantine
  chmod 700 $FILE
  clamscan -f $FILE >> ~/virus.log
  echo $FILE >> ~/virus.log
  mv $FILE ~/autoAIP
done
