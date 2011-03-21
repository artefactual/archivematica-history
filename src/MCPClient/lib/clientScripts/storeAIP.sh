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

set -e

AIP="$1"
bname="`basename "$1"`"
AIPsStore="$2"

mv "$AIP" "${AIPsStore}."
mkdir "/tmp/${bname}"
7z x -bd -o"/tmp/${bname}" "${AIPsStore}${bname}/*.zip"
cd "/tmp/${bname}/"
cd `ls`
md5deep -x ./tagmanifest-md5.txt ./bagit.txt ./bag-info.txt manifest-md5.txt
md5deep -r -x ./manifest-md5.txt ./data

#"`dirname "$0"checkAIPIntegrity.py`" 
rm -r "/tmp/${bname}/"

exit $?
