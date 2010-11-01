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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

etc="$1/etc/archivematicaMCPClient/"
bin="$1/usr/bin/"
lib="$1/usr/local/lib/"
var="$1/usr/local/var/"
share="$1/usr/local/share/"

cp runArchivematicaTranscoder.sh "${bin}"

cp etc "${etc}"

cp *.py "${lib}" #I'm not sure this is the right location.
cp mcpModules "${lib}"

cp clientScripts "${lib}" #I'm not sure this is the right location.

cp share "${share}"






