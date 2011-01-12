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

#source /etc/archivematica/archivematicaConfig.conf

echo Please enter sudo password, if you have not already done so.
sudo echo Thank you.

op="`netstat -l | grep 8100`"
if [ -z "$op" ]; then
	echo starting OpenOffice in listening mode on TCP port 8100.

	#I found these scripts @ http://www.oooninja.com/2008/02/batch-command-line-file-conversion-with.html
	#Posted by Andrew Z at Wednesday, February 27, 2008
	#!/bin/bash 
	# Try to autodetect OOFFICE and OOOPYTHON. 
	OOFFICE=`ls /usr/bin/openoffice.org2.4 /usr/bin/ooffice /usr/lib/openoffice/program/soffice | head -n 1` 
	OOOPYTHON=`ls /opt/openoffice.org*/program/python /usr/bin/python | head -n 1` 
	if [ ! -x "$OOFFICE" ] ; then 
	    echo "Could not auto-detect OpenOffice.org binary" 
	    exit 
	fi 
	if [ ! -x "$OOOPYTHON" ]; then 
	    echo "Could not auto-detect OpenOffice.org Python" 
	    exit 
	fi 
	echo "Detected OpenOffice.org binary: $OOFFICE" 
	echo "Detected OpenOffice.org python: $OOOPYTHON" 
	# Reference: http://wiki.services.openoffice.org/wiki/Using_Python_on_Linux 
	# If you use the OpenOffice.org that comes with Fedora or Ubuntu, uncomment the following line: 
	export PYTHONPATH="/usr/lib/openoffice.org/program" 
	# If you want to simulate for testing that there is no X server, uncomment the next line. 
	unset DISPLAY 
	# Kill any running OpenOffice.org processes. 
	killall -u `whoami` -q soffice 
	# Download the converter script if necessary. 
	#test -f DocumentConverter.py || wget http://www.artofsolving.com/files/DocumentConverter.py 
	# Start OpenOffice.org in listening mode on TCP port 8100. 
	sudo $OOFFICE "-accept=socket,host=localhost,port=8100;urp;StarOffice.ServiceManager" -norestore -nofirststartwizard -nologo -headless & 
	# Wait a few seconds to be sure it has started. 
	sleep 6 
fi

sudo -u archivematica /usr/lib/archivematica/MCPClient/archivematicaClient.py

