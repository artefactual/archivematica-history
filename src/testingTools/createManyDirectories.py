#!/usr/bin/python -OO

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
# @subpackage Testing
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import sys
try:
    max = int(sys.argv[1])
except:
    max = 1000
i = 0
str = "."
while i < max:
    str = "%s/%d" % (str, i)
    os.mkdir(str)
    i +=1

FILE = open(str + "/testfile.txt","w")
FILE.writelines("testText")
FILE.close()

for directory, subDirectories, files in os.walk("./0"):
    for file in files:
        filePath = os.path.join(directory, file)
        print filePath
     