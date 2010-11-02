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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

etc="$1/etc/archivematicaMCPServer/"
bin="$1/usr/bin/"
lib="$1/usr/local/lib/"
var="$1/usr/local/var/"

cp ./runArchivematicaMCPServer.sh "${bin}"

cp -r ./etc "${etc}"

cp ./*.py "${lib}" #I'm not sure this is the proper location.
cp -r ./mcpModules "${lib}."
#chroot $1 ln -s "${lib}mcpModules" /usr/lib/pymodules/python2.6/.

cp -r ./sharedDirectoryStructure "${var}"
#Should we link these to the new shared folder structure?
#chroot $1 mkdir /home/demo/2-reviewSIP
#chroot $1 mkdir /home/demo/3-quarantineSIP
#chroot $1 mkdir /home/demo/4-appraiseSIP
#chroot $1 mkdir /home/demo/5-prepareAIP
#chroot $1 mkdir /home/demo/6-reviewAIP	
#chroot $1 mkdir /home/demo/8-reviewDIP
#chroot $1 mkdir /home/demo/9-uploadDIP
#chroot $1 mkdir /home/demo/ingestLogs
#chroot $1 mkdir /home/demo/SIPerrors
#chroot $1 mkdir /home/demo/SIPerrors/normalizationErrors
#chroot $1 mkdir /home/demo/SIPerrors/possibleVirii
#chroot $1 mkdir /home/demo/SIPerrors/rejectedSIPs
#chroot $1 mkdir /var/7-storeAIP
#chroot $1 mkdir /var/1-receiveSIP
#chroot $1 ln -s /var/7-storeAIP/ /home/demo
#chroot $1 ln -s /var/1-receiveSIP/ /home/demo

#chroot $1 chown -R archivematica:archivematica /home/demo/sharedFolders



