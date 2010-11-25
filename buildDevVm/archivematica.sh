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
# @subpackage Configuration
# @author Austin Trask <austin@artefactual.com>
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

srcDirecotory="../src/"
lib="$1/usr/lib/archivematica/"
var="$1/var/archivematica/"

mkdir $lib
mkdir $var

startDirectory="`pwd`"
echo Start Directory: $startDirectory  1>&2

chroot $1 /etc/init.d/mysql start

cd includes
./vmInstaller-dcb.sh "$1"
./vmInstaller-enviroment.sh "$1"
./vmInstaller-ica-atom.sh "$1"
./vmInstaller-qubit.sh "$1"




#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
chroot $1 adduser --uid 333 --group --system --no-create-home --disabled-login archivematica
chroot $1 gpasswd -a demo archivematica

#Configure chroot $1ers for mcp and client
chroot $1 echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod" >> /etc/chroot $1er





chroot $1 svn co http://archivematica.googlecode.com/svn/trunk/ /home/demo/trunk/src
chroot $1 mkdir /etc/archivematica
chroot $1 mkdir /usr/lib/archivematica

chroot $1 ln -s "/home/demo/trunk/src/MCPServer/etc" "/etc/archivematica/MCPServer"
chroot $1 ln -s "/home/demo/trunk/src/MCPClient/etc" "/etc/archivematica/MCPClient"
chroot $1 ln -s "/home/demo/trunk/src/transcoder/etc" "/etc/transcoder"


chroot $1 ln -s "/home/demo/trunk/src/MCPServer/lib/" "/usr/lib/archivematica/MCPServer"
chroot $1 ln -s "/home/demo/trunk/src/MCPClient/lib/" "/usr/lib/archivematica/MCPClient"
chroot $1 ln -s "/home/demo/trunk/src/transcoder/lib/" "/usr/lib/transcoder"
chroot $1 ln -s "/home/demo/trunk/src/easy-extract/lib/" "/usr/lib/easy-extract"

chroot $1 ln "/home/demo/trunk/src/MCPServer/runArchivematicaMCPServer.sh" "/usr/bin/"
chroot $1 ln "/home/demo/trunk/src/MCPClient/runArchivematicaMCPClient.sh" "/usr/bin/"
chroot $1 ln "/home/demo/trunk/src/easy-extract/bin/easy-extract" "/usr/bin/"
chroot $1 ln "/home/demo/trunk/src/transcoder/bin/transcoder" "/usr/bin/"

chroot $1 ln "/home/demo/trunk/src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/archivematica/MCPServer"
chroot $1 ln "/home/demo/trunk/src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/archivematica/MCPClient"
chroot $1 ln "/home/demo/trunk/src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/transcoder"

chroot $1 mkdir /var/archivematica/
chroot $1 ln -s "/home/demo/trunk/src/MCPServer/sharedDirectoryStructure" "/var/archivematica/sharedDirectory"
chroot $1 chown -R archivematica:archivematica "/var/archivematica/sharedDirectory"
chroot $1 chmod -R g+s "/var/archivematica/sharedDirectory"




#cd "$startDirectory"
#cd "${srcDirecotory}dashboard"
#echo `pwd` 1>&2
#./vmInstaller.sh "$1"

#cd "$startDirectory"
#cd "${srcDirecotory}loadConfig"
#echo `pwd` 1>&2
#./vmInstaller.sh "$1"

#cd "$startDirectory"
#cd "${srcDirecotory}MCPServer"
#echo `pwd` 1>&2
#./vmInstaller.sh "$1"

#cd "$startDirectory"
#cd "${srcDirecotory}MCPClient"
#echo `pwd` 1>&2
#./vmInstaller.sh "$1"

#cd "$startDirectory"
#cd "${srcDirecotory}transcoder"
#echo `pwd` 1>&2
#./vmInstaller.sh "$1"


