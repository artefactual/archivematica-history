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
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

target=$1
UUID=`uuid -v 4`
targetBasename=`basename "$target"`
targetDirname=`dirname "$target"`
newDir="${targetDirname}/${targetBasename}-${UUID}/"
mkdir "${newDir}"
mv "${target}" "${newDir}objects/"
mkdir "${newDir}logs"
mkdir "${newDir}logs/SIPEvents"
mkdir "${newDir}logs/fileMeta"
echo $UUID > "${newDir}logs/SIP-UUID.txt"
mv "${newDir}objects/ArchivematicaQuarantineEvent.xml" "${newDir}logs/SIPEvents/."
mv "${newDir}objects/ArchivematicaUnquarantineEvent.xml" "${newDir}logs/SIPEvents/."



