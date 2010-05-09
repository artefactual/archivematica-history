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

    #Create SIP uuid
    UUID=`uuid`

    #Create Log directories and move SIP to /tmp for processing
    mkdir /home/demo/ingestLogs/$UUID
    mkdir /tmp/$UUID		
    mv "$FILE" /tmp/$UUID/.
    chmod 700 /tmp/$UUID/*

    #if SIP.xml does not exist then create initial structure 
    if [ ! -f /tmp/$UUID/SIP.xml ]
    then
      tmpDir=`pwd`
      cd /tmp/$UUID/
      /opt/archivematica/SIPxmlModifiers/CreateSipAndAddDublinCoreStructure.py
      cd $tmpDir	
    fi
    
    #move newly created SIP.xml to logs directory
    mv /tmp/$UUID/SIP.xml /home/demo/ingestLogs/$UUID/SIP.xml

    #extract all of the .zip .rar etc.
    python /opt/externals/easy-extract/easy_extract.py /tmp/$UUID/ -w -f -r -n 2>&1 >> /home/demo/ingestLogs/$UUID/extraction.log

    #Add initial file structure to SIP.xml  run detox and add cleaned file structure to SIP.xml
    /opt/archivematica/SIPxmlModifiers/addFileStructureToSIP.py "/home/demo/ingestLogs/$UUID" $UUID
    /opt/archivematica/SIPxmlModifiers/addUUIDasDCidentifier.py "/home/demo/ingestLogs/$UUID" $UUID
    detox -rv /tmp/$UUID >> /home/demo/ingestLogs/$UUID/detox.log
    cleanName=`ls /tmp/$UUID`
    /opt/archivematica/SIPxmlModifiers/addDetoxLogToSIP.py "/home/demo/ingestLogs/$UUID" "$FILE"

    #Scan SIP for virri and run fits for file identification
    find /tmp/$UUID/ -type f -print| while read NEWDOCS
      do
        # XENADIR=`dirname "$NEWDOCS"`  # needed if using normalize.sh				
        chmod 700 $NEWDOCS
        clamscan --move=/home/demo/SIPerrors/possibleVirii/  $NEWDOCS >> ~/ingestLogs/$UUID/virusSCAN.log
        /opt/archivematica/folderaccess.sh  $NEWDOCS $UUID  # run  FITS
        echo "Receipt of $NEWDOCS completed" >> ~/ingestLogs/accession.log
      done

    #copy logs directory to SIP
    cp -a /home/demo/ingestLogs/$UUID /tmp/$UUID/$cleanName/ingestLogs		

    #move processed SIP to 4-appraiseSIP and notify user of completion
    mv /tmp/$UUID/$cleanName /home/demo/4-appraiseSIP/$cleanName-$UUID
    DISPLAY=:0.0 /usr/bin/notify-send "ingest" "$cleanName ready for appraisal"

    #cleanup
    rm -rf /tmp/$UUID
  elif [ -f "$FILE" ]; then
    chmod 700 "$FILE"
    mv "$FILE" /home/demo/SIPerrors/.
    DISPLAY=:0.0 /usr/bin/notify-send "SIP Error" "A SIP must be submitted as a directory"
  else
    echo "$FILE is not a file or directory"
  fi
done
