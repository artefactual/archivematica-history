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

#rm /home/$USER/.config/Thunar/uca.xml; ./addArchivematicaGUIScripts.sh 

set -e
add="`dirname $0`/src/add.sh"
UCA="/home/$USER/.config/Thunar/uca.xml"
if [ -f "$UCA" ]
then
	echo "Appending for file $UCA." 
else
	echo "Creating $UCA."
	echo "<actions>"  > "$UCA"
	echo "</actions>" >> "$UCA" 
fi


"$add" \
	--icon="accessories-calculator" \
	--name="SIP-Restructure For Compliance" \
	--command="archivematicaRestructureForCompliance %F/" \
	--description="Restructure For Compliance" \
	--directories

"$add" \
	--icon="accessories-calculator" \
	--name="SIP-Create DC" \
	--command="cd %F/metadata && createDublinCore %F/" \
	--description="Insert a blank Dublin Core XML into metadata directory" \
	--directories	

"$add" \
	--icon="accessories-calculator" \
	--name="SIP-Create md5 checksum" \
	--command="archivematicaCreateMD5 %F | zenity --progress --pulsate --auto-close --auto-kill" \
	--description="Create MD5 checksums for all the selected files in this folder" \
	--directories

"$add" \
	--icon="accessories-calculator" \
	--name="SIP-Do All" \
	--command="archivematicaRestructureForCompliance %F/ && archivematicaCreateMD5 %F | zenity --progress --pulsate --auto-close --auto-kill && cd %F/metadata && createDublinCore %F/" \
	--description="Restructures, creates MD5 and DC" \
	--directories

#"$add" \
#	--icon="accessories-calculator" \
#	--name="Remove as ROOT" \
#	--command="gksudo -u root \"rm -r -f %F\"" \
#	--description="Does a sudo remove of the file/directory. (Recursive & Force)" \
#    --directories

"$add" \
    --icon="accessories-calculator" \
    --name="Set Ownership and Permissions" \
    --command="gksudo \"chown -R archivematica:archivematica %F\" && gksudo \"chmod -R 770 %F\"" \
    --description="Set ownership to archivematica:archivematica and permissions to 770" \
    --directories --audioFiles --imageFiles --otherFiles --textFiles --videoFiles

"$add" \
    --icon="accessories-calculator" \
    --name="Open terminal here" \
    --command="xfce4-terminal --default-working-directory=%d" \
    --description="Opens a terminal at this directory" \
    --directories --audioFiles --imageFiles --otherFiles --textFiles --videoFiles
    
#"$add" \
#    --icon="accessories-calculator" \
#    --name="Save path to clipboard" \
#    --command="echo -n %f | xclip -i" \
#    --description="" \
#    --directories --audioFiles --imageFiles --otherFiles --textFiles --videoFiles
#http://forum.xfce.org/viewtopic.php?id=3215
	

"$add" \
    --icon="accessories-calculator" \
    --name="Create a structured directory" \
    --command="/usr/lib/archivematica/archivematicaCommon/archivematicaCreateStructuredDirectory.sh %d" \
    --description="Creates a structured directory for archivematica processing" \
    --directories 
