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

#move sip to /tmp
mv /home/demo/5-prepareAIP/$2 /tmp/$2

#parse line for uuid and sip name
length=`expr length $2`
position=$length-36
UUID=${2:$position}

mkdir /tmp/$UUID
mkdir /tmp/$UUID/objects

DISPLAY=:0.0 /usr/bin/notify-send "Normalizing" "Converting files in $2 to preservation and access formats"
#read folder structure and run normalize.py on files
  find /tmp/$2/objects -type f -exec python /opt/archivematica/normalize.py {} /tmp/$UUID/objects \; -print >>/tmp/$2/logs/normalization.log 2>&1 

#use baggit to create AIP
DISPLAY=:0.0 /usr/bin/notify-send "Preparing AIP" "Creating Bagit package for $2"
/opt/externals/bagit/bin/bag create /home/demo/6-reviewAIP/$2.zip /tmp/$2/* --writer zip

cp ~/ingestLogs/$UUID/METS.xml /tmp/$UUID
mv /tmp/$UUID /home/demo/8-reviewDIP/$2

#cleanup
rm -rf /tmp/$2

#notify user that AIP creation is complete
DISPLAY=:0.0 /usr/bin/notify-send "AIP prepared" "AIP $2 ready for review"
