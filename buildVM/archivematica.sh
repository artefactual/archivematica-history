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

echo $startDirectory

cd includes
./vmInstaller-dcb.sh "$1"
./vmInstaller-enviroment.sh "$1"
./vmInstaller-ica-atom.sh "$1"
./vmInstaller-qubit.sh "$1"


cd "$startDirectory"
cd "${srcDirecotory}dashboard"
echo `pwd`
./vmInstaller.sh "$1"

cd "$startDirectory"
cd "${srcDirecotory}loadConfig"
echo `pwd`
./vmInstaller.sh "$1"

cd "$startDirectory"
cd "${srcDirecotory}MCPServer"
echo `pwd`
./vmInstaller.sh "$1"

cd "$startDirectory"
cd "${srcDirecotory}MCPClient"
echo `pwd`
./vmInstaller.sh "$1"

cd "$startDirectory"
cd "${srcDirecotory}transcoder"
echo `pwd`
./vmInstaller.sh "$1"


