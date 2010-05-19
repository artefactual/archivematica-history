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
MD5FILE="MD5checksum.txt"

find ~/3-quarantineSIP/* -maxdepth 0 -amin +1 -perm 0000 -print| while read FILE

do
  if [ -d "$FILE" ]; then
    chmod 700 "$FILE"		

    # Create SIP uuid
    UUID=`uuid -v 4`

    BASENAME=`basename "$FILE"`

    echo "$UUID -> $BASENAME"

    DISPLAY=:0.0 /usr/bin/notify-send "Quarantine completed" "Preparing $BASENAME for appraisal"
    # Create Log directories and move SIP to /tmp for processing
    mkdir /home/demo/ingestLogs/$UUID
    mkdir /tmp/$UUID		
    mv "$FILE" /tmp/$UUID/.
    chmod 700 -R /tmp/$UUID/

    # If DublinCore.xml does not exist then create it
    if [ ! -f "/tmp/$UUID/$BASENAME/DublinCore.xml" ]
    then
      tmpDir=`pwd`
      cd "/tmp/$UUID/$BASENAME"
      /opt/archivematica/xmlScripts/createDublinCore.py
      cd $tmpDir	
    fi
    # Move DublinCore.xml to logs directory
    mv "/tmp/$UUID/$BASENAME/DublinCore.xml" "/home/demo/ingestLogs/$UUID/dublincore.xml"

    # If MD5 checksum does not exist then create it
    if [ ! -f "/tmp/$UUID/$BASENAME/$MD5FILE" ]    
    then
      tmpDir=`pwd`
      cd "/tmp/$UUID/$BASENAME"
      md5deep -rl "." > "$MD5FILE"
      cd $tmpDir      
    fi
    mv "/tmp/$UUID/$BASENAME/$MD5FILE" "/home/demo/ingestLogs/$UUID/$MD5FILE"

    #Check MD5s
    /opt/archivematica/checkMD5NoGUI.sh "/tmp/$UUID/$BASENAME/" "/home/demo/ingestLogs/$UUID/$MD5FILE" "/home/demo/ingestLogs/$UUID/$MD5FILE"processSIP_check.log

    # Extract all of the .zip .rar etc.
    DISPLAY=:0.0 /usr/bin/notify-send "Opening packages" "Extracting packages (.zip, .rar, etc.) found in $BASENAME"
    python /opt/externals/easy-extract/easy_extract.py /tmp/$UUID/ -w -f -r -n 2>&1 >> /home/demo/ingestLogs/$UUID/extraction.log

    # Clean filenames
    DISPLAY=:0.0 /usr/bin/notify-send "Cleaning file names" "Cleaning up prohibited file name characters found in $BASENAME"
    detox -rv /tmp/$UUID >> /home/demo/ingestLogs/$UUID/filenameCleanup.log
    cleanName=`ls /tmp/$UUID`

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
        FileUUID=`uuid -v 4`
        /opt/archivematica/runFITS.sh  $NEWDOCS $UUID $FileUUID
        echo "$FileUUID -> `/opt/archivematica/fileUUID.py "Logline" "/tmp/$UUID/$cleanName" "$NEWDOCS"`" >> ~/ingestLogs/$UUID/FileUUIDs.log
        echo "`date +%F" "%T` `basename $NEWDOCS`" >> ~/ingestLogs/$UUID/FITS.log
        #the following line works to read uuid from the uuid log
        #echo "`basename $NEWDOCS` assigned UUID: `/opt/archivematica/fileUUID.py "getFileUUID" "$UUID" "/tmp/$UUID/$cleanName" "$NEWDOCS"`"
      done

    # Create METS.XML
    # NOTE: the detoxed name of FILE needs to be sent to this script $3
    /opt/archivematica/xmlScripts/createMETS.py "/home/demo/ingestLogs/$UUID" $UUID $cleanName

    # Insert DublinCore.XML into METS.XML
    #/opt/archivematica/xmlScripts/addDublinCoreToMETS.py /home/demo/ingestLogs/$UUID /home/demo/ingestLogs/$UUID
    
    mkdir /home/demo/4-appraiseSIP/$cleanName-$UUID    

    # Copy logs directory to SIP
    cp -a /home/demo/ingestLogs/$UUID /home/demo/4-appraiseSIP/$cleanName-$UUID/logs
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
