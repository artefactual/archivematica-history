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

checkMD5NoGui="`dirname $0`/archivematicaCheckMD5NoGUI.sh"

target="$1"
checksums="$2"
date="$3"
eventID="$4"
MD5FILE="${target}metadata/${checksums}.md5"

ret=0

if [ -f "${MD5FILE}" ]; then
    "${checkMD5NoGui}" "${target}objects/" "${MD5FILE}" "${target}logs/`basename "${MD5FILE}"`-Check-`date`" && \
    "`dirname $0`/createXMLeventsMD5Verified.py" "$eventID" "$date" "`md5deep -v`" "md5deep" "${target}"  
    ret+="$?"
else
    echo "File Does not exist:" "${MD5FILE}"
fi


exit ${ret}


