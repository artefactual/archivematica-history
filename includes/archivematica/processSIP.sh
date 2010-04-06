#!/bin/bash

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.


# @package Archivematica
# @subpackage Ingest
# @author Austin Trask <austin@artefactual.com>
# @version svn: $Id$

find ~/3-quarantine/* -maxdepth 0 -amin +1 -perm 0000 -print| while read FILE
do
	if [ -d "$FILE" ]; then
		chmod 700 "$FILE"		
		UUID=`uuid`
		mkdir /home/demo/ingestLogs/$UUID		
		mv "$FILE" /tmp/$UUID
		chmod 700 /tmp/$UUID/*
		#extract all of the .zip .rar etc.
		python /opt/externals/easy-extract/easy_extract.py /tmp/$UUID/ -w -f -r -n 2>&1 >> /home/demo/ingestLogs/$UUID/extraction.log
		cd /tmp/$UUID; /opt/archivematica/SIPxmlModifiers/addFileStructureToSIP.py >> /home/demo/ingestLogs/$UUID/SIP.xml
		detox -rv /tmp/$UUID >> /home/demo/ingestLogs/$UUID/detox.log
		python /opt/archivematica/SIPxmlModifiers/addDetoxLogToSIP.py "/home/demo/ingestLogs/$UUID/"
		find /tmp/$UUID/ -type f -print| while read NEWDOCS
			do
				XENADIR=`dirname "$NEWDOCS"`				
				chmod 700 $NEWDOCS
				clamscan --move=/home/demo/possiblevirii/  $NEWDOCS >> ~/ingestLogs/$UUID/virusSCAN.log
				/opt/archivematica/folderaccess.sh  $NEWDOCS $UUID 
				echo "Accession of $NEWDOCS completed successfully" >> ~/ingestLogs/accession.log
				/opt/archivematica/normalize.sh $NEWDOCS $XENADIR $UUID
			done
		cp -a /home/demo/ingestLogs/$UUID /tmp/$UUID/ingestLogs		
		BASEFILE=`basename "$FILE"`
		/opt/externals/bagit/bin/bag create /home/demo/4-appraiseSIP/"$BASEFILE"-$UUID.zip /tmp/$UUID/* --writer zip
		/opt/archivematica/upload/upload-qubit.py -d --email=demo@example.com --password=demo --title="$BASEFILE" --file=/home/demo/4-appraiseSIP/"$BASEFILE"-"$UUID".zip
		rm -rf /tmp/$UUID
		DISPLAY=:0.0 /usr/bin/notify-send "ingest" "ingest of $BASEFILE completed"
	elif [ -f "$FILE" ]; then
		chmod 700 "$FILE"
		mv "$FILE" /home/demo/SIPerrors/.
		DISPLAY=:0.0 /usr/bin/notify-send "SIP Error" "A SIP must be submitted as a directory"
	else
		echo "$FILE is not a file or directory"
	fi
done
