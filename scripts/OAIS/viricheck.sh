#!/bin/bash

find ~/quarantine/* -amin +2 -print| while read FILE
do
  #move file to quarantine
  chmod 700 $FILE
  clamscan  $FILE >> ~/virus.log
  echo "\n" >> ~/virus.log
  mv $FILE ~/autoAIP
done
