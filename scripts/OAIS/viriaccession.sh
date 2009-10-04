#!/bin/bash

find ~/quarantine/* -amin +4 -print| while read FILE
do
	chmod 700 $FILE
	if [ -d "$FILE" ]; then
		NOW=`date +%s`
		mkdir /home/demo/accessionrecords/$NOW		
		mkdir -p /tmp/accession-$NOW
		mv $FILE /tmp/accession-$NOW
		chmod -R 700 /tmp/accession-$NOW/*
		find /tmp/accession-$NOW/ -type f -print| while read NEWDOCS
			do
				/usr/local/OAIS/fits/folderaccess.sh  $NEWDOCS $NOW 
				clamscan --move=/home/demo/possiblevirii/  $NEWDOCS >> ~/accessionrecords/$NOW/virus.log
				echo "Acession of $NEWDOCS completed successfully" >> ~/accessionrecords/accession.log
			done		
		mv /tmp/accession-$NOW/* ~/normalizeMe/.
		rm -rf /tmp/accession-$NOW
	elif [ -f "$FILE" ]; then
		NOW=`date +%s`
		mkdir /home/demo/accessionrecords/$NOW
		/usr/local/OAIS/fits/access.sh $FILE $NOW
		clamscan --move=/home/demo/possiblevirii/  $FILE >> ~/accessionrecords/$NOW/virus.log		
		mv $FILE ~/normalizeMe/.
		echo "Acession of $FILE completed successfully" >> ~/accessionrecords/accession.log
	else
		echo "$FILE is not a file or directory"
	fi
done
