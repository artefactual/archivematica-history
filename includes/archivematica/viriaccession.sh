#!/bin/bash

find ~/quarantine/* -maxdepth 0 -amin +2 -perm 0000 -print| while read FILE
do
	if [ -d "$FILE" ]; then
		chmod 700 $FILE		
		UUID=`uuid`
		mkdir /home/demo/accessionreports/$UUID		
		mkdir -p /tmp/accession-$UUID
		mv $FILE /tmp/accession-$UUID
		chmod 700 /tmp/accession-$UUID/*
		find /tmp/accession-$UUID/ -type f -print| while read NEWDOCS
			do
				chmod 700 $NEWDOCS
				clamscan --move=/home/demo/possiblevirii/  $NEWDOCS >> ~/accessionreports/virus.log
				/opt/externals/fits/folderaccess.sh  $NEWDOCS $UUID 
				echo "Acession of $NEWDOCS completed successfully" >> ~/accessionreports/accession.log
			done		
		mv /tmp/accession-$UUID/* ~/prepareAIP/.
		rm -rf /tmp/accession-$UUID
	elif [ -f "$FILE" ]; then
		chmod 700 $FILE		
		UUID=`uuid`
		mkdir /home/demo/accessionreports/$UUID
		clamscan --move=/home/demo/possiblevirii/  $FILE >> ~/accessionreports/virus.log		
		/opt/externals/fits/access.sh $FILE $UUID		
		mv $FILE ~/prepareAIP/.
		echo "Accession of $FILE completed successfully" >> ~/accessionreports/accession.log
	else
		echo "$FILE is not a file or directory"
	fi
done
