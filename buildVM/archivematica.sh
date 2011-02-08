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


cd "$startDirectory"
cd "${srcDirecotory}dashboard"
echo `pwd` 1>&2
./vmInstaller.sh "$1"

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


