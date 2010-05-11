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

#read folder structure and run normalize.py on files
find /tmp/$2/ -type f -print| while read NEWDOCS
  do
#    /opt/archivematica/normalize.py $NEWDOCS $UUID >> `dirname $NEWDOCS`/normalization.log 2>&1
    /opt/archivematica/normalize.py $NEWDOCS $UUID >> /tmp/$2/normalization.log 2>&1
  done

sleep 5 #Allow finish writing to the normalization.log file

#use baggit to create AIP
/opt/externals/bagit/bin/bag create /home/demo/6-reviewAIP/$2.zip /tmp/$2/* --writer zip

#cleanup
rm -rf /tmp/$2

#notify user that AIP creation is complete
DISPLAY=:0.0 /usr/bin/notify-send "prepareAIP" "$2 AIP ready for review"
