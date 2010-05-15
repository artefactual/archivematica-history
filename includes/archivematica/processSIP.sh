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
# @author Joseph Perry <joseph@artefactual.com>
# @author Peter Van Garderen <peter@artefactual.com>
# @version svn: $Id$

#find ~/3-quarantineSIP/* -maxdepth 0 -perm 0000 -print| while read FILE
find ~/3-quarantineSIP/* -maxdepth 0 -amin +1 -perm 0000 -print| while read FILE
do
  if [ -d "$FILE" ]; then
    chmod 700 "$FILE"		

    # Create SIP uuid
    UUID=`uuid`

    BASENAME=`basename "$FILE"`

    DISPLAY=:0.0 /usr/bin/notify-send "Quarantine completed" "Preparing $BASENAME for appraisal"
    # Create Log directories and move SIP to /tmp for processing
    mkdir /home/demo/ingestLogs/$UUID
    mkdir /tmp/$UUID		
    mv "$FILE" /tmp/$UUID/.
    chmod 700 -R /tmp/$UUID/

    # If SIP.xml does not exist then create initial structure 
    if [ ! -f "/tmp/$UUID/$BASENAME/SIP.xml" ]
    then
      tmpDir=`pwd`
      cd "/tmp/$UUID/$BASENAME"
      /opt/archivematica/SIPxmlModifiers/CreateSipAndAddDublinCoreStructure.py
      cd $tmpDir	
    fi
    # Move SIP.xml to logs directory
    mv "/tmp/$UUID/$BASENAME/SIP.xml" "/home/demo/ingestLogs/$UUID/SIP.xml"

    # If DublinCore.xml does not exist then create initial structure 
    if [ ! -f "/tmp/$UUID/$BASENAME/DublinCore.xml" ]
    then
      tmpDir=`pwd`
      cd "/tmp/$UUID/$BASENAME"
      /opt/archivematica/xmlScripts/createDublinCore.py
      cd $tmpDir	
    fi
    # Move DublinCore.xml to logs directory
    mv "/tmp/$UUID/$BASENAME/DublinCore.xml" "/home/demo/ingestLogs/$UUID/DublinCore.xml"

    # Create METS.XML
    tmpDir=`pwd`
    cd "/home/demo/ingestLogs/$UUID"
    /opt/archivematica/xmlScripts/createMETS.py
     cd $tmpDir

    # Insert DublinCore.XML into METS.XML
    # /opt/archivematica/xmlScripts/addDublinCoreToMETS.py

    # Extract all of the .zip .rar etc.
    DISPLAY=:0.0 /usr/bin/notify-send "Opening packages" "Extracting packages (.zip, .rar, etc.) found in $BASENAME"
    python /opt/externals/easy-extract/easy_extract.py /tmp/$UUID/ -w -f -r -n 2>&1 >> /home/demo/ingestLogs/$UUID/extraction.log

    # Add initial file structure to SIP.xml  run detox and add cleaned file structure to SIP.xml
    /opt/archivematica/SIPxmlModifiers/addFileStructureToSIP.py "/home/demo/ingestLogs/$UUID" $UUID
    /opt/archivematica/SIPxmlModifiers/addUUIDasDCidentifier.py "/home/demo/ingestLogs/$UUID" $UUID

    # Add fileSec to METS.XML
    /opt/archivematica/xmlScripts/addFileSecToMETS.py "/home/demo/ingestLogs/$UUID" $UUID

    # Clean filenames
    DISPLAY=:0.0 /usr/bin/notify-send "Cleaning file names" "Cleaning up illegal file name characters found in $BASENAME"
    detox -rv /tmp/$UUID >> /home/demo/ingestLogs/$UUID/filenameCleanup.log
    cleanName=`ls /tmp/$UUID`
    /opt/archivematica/SIPxmlModifiers/addDetoxLogToSIP.py "/home/demo/ingestLogs/$UUID" "$FILE"

    # Scan SIP for virri
    DISPLAY=:0.0 /usr/bin/notify-send "Virus scan" "Checking for viruses in $BASENAME"
    find /tmp/$UUID/ -type f -print| while read NEWDOCS
      do
        chmod 700 $NEWDOCS
	# DISPLAY=:0.0 /usr/bin/notify-send "Virus scan" "checking `basename $NEWDOCS`"
        clamscan --move=/home/demo/SIPerrors/possibleVirii/  $NEWDOCS >> ~/ingestLogs/$UUID/virusScan.log
      done

    # Run FITS for file identification, validation and metadata extraction
    DISPLAY=:0.0 /usr/bin/notify-send "Format identification" "Identifiying, validating and extracting metadata from objects in $BASENAME"
    find /tmp/$UUID/ -type f -print| while read NEWDOCS
      do
        chmod 700 $NEWDOCS
        /opt/archivematica/runFITS.sh  $NEWDOCS $UUID
        echo "`date +%F" "%T` `basename $NEWDOCS`" >> ~/ingestLogs/$UUID/FITS.log
      done
    
    mkdir /home/demo/4-appraiseSIP/$cleanName-$UUID    

    # Copy logs directory to SIP
    cp -a /home/demo/ingestLogs/$UUID /home/demo/4-appraiseSIP/$cleanName-$UUID/logs
    mv /home/demo/4-appraiseSIP/$cleanName-$UUID/logs/SIP.xml /home/demo/4-appraiseSIP/$cleanName-$UUID/
    mv /home/demo/4-appraiseSIP/$cleanName-$UUID/logs/METS.xml /home/demo/4-appraiseSIP/$cleanName-$UUID/

    # Move processed SIP to 4-appraiseSIP and notify user of completion
    mv /tmp/$UUID/$cleanName /home/demo/4-appraiseSIP/$cleanName-$UUID/objects
    DISPLAY=:0.0 /usr/bin/notify-send "SIP processing completed" "$cleanName ready for appraisal"

    # Cleanup
    rm -rf /tmp/$UUID
  elif [ -f "$FILE" ]; then
    chmod 700 "$FILE"
    mv "$FILE" /home/demo/SIPerrors/.
    DISPLAY=:0.0 /usr/bin/notify-send "SIP Error" "A SIP must be submitted as a directory. Files moved to SIPerrors folder."
  else
    echo "$FILE is not a file or directory"
  fi
done
