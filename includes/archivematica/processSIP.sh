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

find ~/3-quarantineSIP/* -maxdepth 0 -amin +1 -perm 0000 -print| while read FILE
do
	if [ -d "$FILE" ]; then
		chmod 700 "$FILE"		
		UUID=`uuid`
		mkdir /home/demo/ingestLogs/$UUID		
		mv "$FILE" /tmp/$UUID
		chmod 700 /tmp/$UUID/*
		if [ ! -f /tmp/$UUID/SIP.xml ]
		then
			tmpDir=`pwd`
			cd /tmp/$UUID/
			/opt/archivematica/SIPxmlModifiers/CreateSipAndAddDublinCoreStructure.py
			cd $tmpDir
			
		fi
		mv /tmp/$UUID/SIP.xml /home/demo/ingestLogs/$UUID/SIP.xml
		
		#extract all of the .zip .rar etc.
		python /opt/externals/easy-extract/easy_extract.py /tmp/$UUID/ -w -f -r -n 2>&1 >> /home/demo/ingestLogs/$UUID/extraction.log
		/opt/archivematica/SIPxmlModifiers/addFileStructureToSIP.py "/home/demo/ingestLogs/$UUID" $UUID
		/opt/archivematica/SIPxmlModifiers/addUUIDasDCidentifier.py "/home/demo/ingestLogs/$UUID" $UUID
		detox -rv /tmp/$UUID >> /home/demo/ingestLogs/$UUID/detox.log
		python /opt/archivematica/SIPxmlModifiers/addDetoxLogToSIP.py "/home/demo/ingestLogs/$UUID" "$FILE"
		find /tmp/$UUID/ -type f -print| while read NEWDOCS
			do
				# XENADIR=`dirname "$NEWDOCS"`  # needed if using normalize.sh				
				chmod 700 $NEWDOCS
				clamscan --move=/home/demo/SIPerrors/possibleVirii/  $NEWDOCS >> ~/ingestLogs/$UUID/virusSCAN.log
				/opt/archivematica/folderaccess.sh  $NEWDOCS $UUID  # run  FITS
				echo "Receipt of $NEWDOCS completed" >> ~/ingestLogs/accession.log
				# /opt/archivematica/normalize.py $NEWDOCS $UUID # move to 5-prepareAIP
			done
		cp -a /home/demo/ingestLogs/$UUID /tmp/$UUID/ingestLogs		
		BASEFILE=`basename "$FILE"`
		mv /tmp/$UUID /home/demo/4-appraiseSIP/"$BASEFILE"-$UUID
		DISPLAY=:0.0 /usr/bin/notify-send "ingest" "$BASEFILE ready for appraisal"
	elif [ -f "$FILE" ]; then
		chmod 700 "$FILE"
		mv "$FILE" /home/demo/SIPerrors/.
		DISPLAY=:0.0 /usr/bin/notify-send "SIP Error" "A SIP must be submitted as a directory"
	else
		echo "$FILE is not a file or directory"
	fi
done
