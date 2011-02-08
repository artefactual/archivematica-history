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
# @subpackage MCP
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


cd "$2"
find ${2}/* -maxdepth 0 -amin "+${1}" -print| while read FILE

do
  	#basedName=`basename "$FILE"`
    if [ -d "$FILE" ]; then
    	echo moving $FILE 
    	mv "$FILE" "$3"  
    fi    
done