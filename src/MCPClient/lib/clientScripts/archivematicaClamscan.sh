#!/bin/bash

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#source /etc/archivematica/archivematicaConfig.conf

target="$1"
eIDValue="$2"
eDate="$3"
fileUUID="$4"
logsDir="$5"
temp="/tmp/`uuid`"
clamscanResultShouldBe="Infected files: 0"

clamscanVersion=`clamdscan -V`
clamdscan  - <"$target" >$temp 
a=$?

if [ 0 -eq $a ] ; then
	clamscanResult=`grep "Infected files" $temp`
	`dirname "$0"`/createXMLEventClamscan.py "$eIDValue" "$eDate" "$clamscanVersion" "$clamscanResult " "$clamscanResultShouldBe " "$fileUUID" "$logsDir"
	b=$?
else
	`dirname "$0"`/createXMLEventClamscan.py "$eIDValue" "$eDate" "$clamscanVersion" "$clamscanResult " "$clamscanResultShouldBe " "$fileUUID" "$logsDir"
	b=$?
fi

let "num = (( $a || $b ))"
if [ 0 -ne $num ] ; then
	echo 1>&2
	echo ${fileUUID}-`basename $target` 1>&2
	cat $temp 1>&2
	echo 1>&2
fi
rm $temp 
exit $num



