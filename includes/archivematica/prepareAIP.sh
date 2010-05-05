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

mv $1/$2 /tmp/$2

length=`expr length $2`
position=$length-36
UUID=${2:$position}

find /tmp/$2/ -type f -print| while read NEWDOCS
  do
    /opt/archivematica/normalize2.py $NEWDOCS $UUID >> `dirname $NEWDOCS`/normalization2.log 2>&1
  done

/opt/externals/bagit/bin/bag create /home/demo/6-reviewAIP/$2.zip /tmp/$2/* --writer zip

rm -rf /tmp/$2

DISPLAY=:0.0 /usr/bin/notify-send "prepareAIP" "$2 AIP ready for review"
