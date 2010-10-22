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
source /etc/archivematica/archivematicaConfig.conf

target="$1"
objectsDir="$2"
eIDValue="$3"
eDate="$4"
eventDirectory="$5"


uuidVersion="4"
fileUUID=`uuid -v ${uuidVersion}`
echo "$fileUUID -> `"$fileUUIDPY" "Logline" "${objectsDir}" "${target}"`"

#eIDValue="$fileUUID"
${clientScriptsDirectory}createXMLEventAssignUUID.py "$eIDValue" "$eDate" "$uuidVersion" "$fileUUID" > "${eventDirectory}ArchivematicaAssignUUID_${fileUUID}_Event.xml"

exit $?

