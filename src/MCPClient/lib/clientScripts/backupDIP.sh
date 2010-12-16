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

DIP="$1"
DIPsStore="${2}`basename $1`/"
uploadedObjects="DIPUploadedFiles.txt"

cd "$DIP"
ls objects > "$uploadedObjects"

mkdir "${DIPsStore}"
mv "objectsBackup" "${DIPsStore}."
chmod -R 750 "$uploadedObjects"
mv "$uploadedObjects" "${DIPsStore}."
chmod 770 "${DIPsStore}${uploadedObjects}"
cp "METS.xml" "${DIPsStore}."