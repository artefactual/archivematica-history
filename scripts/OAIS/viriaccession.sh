#!/bin/bash

find ~/quarantine/* -maxdepth 0 -amin +2 -perm 0000 -print| while read FILE
do
	if [ -d "$FILE" ]; then
		chmod 700 $FILE		
		NOW=`date +%s`
		mkdir /home/demo/accessionreports/$NOW		
		mkdir -p /tmp/accession-$NOW
		mv $FILE /tmp/accession-$NOW
		chmod 700 /tmp/accession-$NOW/*
		find /tmp/accession-$NOW/ -type f -print| while read NEWDOCS
			do
				chmod 700 $NEWDOCS
				clamscan --move=/home/demo/possiblevirii/  $NEWDOCS >> ~/accessionreports/$NOW/virus.log
				/usr/local/OAIS/fits/folderaccess.sh  $NEWDOCS $NOW 
				echo "Acession of $NEWDOCS completed successfully" >> ~/accessionreports/accession.log
			done		
		mv /tmp/accession-$NOW/* ~/prepareAIP/.
		rm -rf /tmp/accession-$NOW
	elif [ -f "$FILE" ]; then
		chmod 700 $FILE		
		NOW=`date +%s`
		mkdir /home/demo/accessionreports/$NOW
		clamscan --move=/home/demo/possiblevirii/  $FILE >> ~/accessionreports/$NOW/virus.log		
		/usr/local/OAIS/fits/access.sh $FILE $NOW		
		mv $FILE ~/prepareAIP/.
		echo "Acession of $FILE completed successfully" >> ~/accessionreports/accession.log
	else
		echo "$FILE is not a file or directory"
	fi
done
