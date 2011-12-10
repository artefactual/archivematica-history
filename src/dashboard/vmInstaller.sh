#!/bin/bash

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
# 
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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

#add archivematica/dashboard icons
#cp includes/desktopShortcuts/dashboard-desktop-icon.png $1/usr/share/icons
#cp includes/dashboard.desktop $1/home/demo/Desktop
#cp ../buildVM/includes/desktopShortcuts/rundashboard.sh $1/usr/bin

chroot $1 mysqladmin create dashboard
svn export src $1/usr/local/share/archivematica-dashboard


