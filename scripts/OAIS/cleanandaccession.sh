#!/bin/bash

find /home/demo/drop/. -type f -print| while read FILE
do
  #Sanatize newly added user files
  file_clean=${FILE//[ ()&\'\,]/_}
  shortcleanfile=`basename "$file_clean"`
  echo $shortcleanfile

  #move file to quarantine
  mv "$FILE" ~/quarantine/$shortcleanfile

  #accession of file
  /usr/local/OAIS/fits/access.sh  ~/quarantine/$shortcleanfile 

  #lock file for quarentine 
  chmod 000 ~/quarantine/$shortcleanfile

done

