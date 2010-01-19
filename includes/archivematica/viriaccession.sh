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
