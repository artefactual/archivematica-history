#!//bin/bash
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
# @subpackage 
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


set -e
add="`dirname $0`/src/add.sh"
"$add" \
	--icon="accessories-calculator" \
	--name="Restructure For Compliance" \
	--command="archivematicaRestructureForCompliance %F/" \
	--description="Restructure For Compliance"

"$add" \
	--icon="accessories-calculator" \
	--name="Create DC" \
	--command="createDublinCore %F/" \
	--description="Insert a blank Dublin Core XML template in this folder"
	

"$add" \
	--icon="accessories-calculator" \
	--name="Create md5 checksum" \
	--command="archivematicaCreateMD5 %F" \
	--description="Create MD5 checksums for all the selected files in this folder"

"$add" \
	--icon="accessories-calculator" \
	--name="Remove as ROOT" \
	--command="gksudo -u root \"rm -r -f %F\"" \
	--description="Does a sudo remove of the file/directory. (Recursive & Force)"

