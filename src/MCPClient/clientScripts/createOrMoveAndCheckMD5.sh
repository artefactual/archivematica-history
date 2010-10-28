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
MD5FILE="$2"
UUID=`uuid -v 4`
targetBasename=`basename "$target"`
targetDirname=`dirname "$target"`

if [ -f "${target}objects/$MD5FILE" ]; then
    mv "${target}objects/$MD5FILE" "${target}logs/${MD5FILE}"
else
    tmpDir=`pwd`
    cd "${target}objects/"
    md5deep -rl "." > "${target}logs/${MD5FILE}"
    cd $tmpDir
fi
"$checkMD5NoGui" "${target}objects/" "${target}logs/${MD5FILE}" "${target}logs/${MD5FILE}-Check-`date`"


