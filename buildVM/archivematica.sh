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

startDirectory="`pwd`"
cd includes
./vminstaller.sh
vminstaller-dcb.sh
vminstaller-enviroment.sh
vminstaller-ica-atom.sh
vminstaller-qubit.sh


cd "$startDIrectory"
cd "${srcDirecotory}dashboard"
./vminstaller.sh

cd "$startDIrectory"
cd "${srcDirecotory}loadConfig"
./vminstaller.sh

cd "$startDIrectory"
cd "${srcDirecotory}MCPServer"
./vminstaller.sh

cd "$startDIrectory"
cd "${srcDirecotory}MCPClient"
./vminstaller.sh

cd "$startDIrectory"
cd "${srcDirecotory}transcoder"
./vminstaller.sh


