#!/usr/bin/python -OO

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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import sys
target = sys.argv[1]
if not os.path.isdir(target):
    print >>sys.stderr, "Directory doesn't exist: ", target
    os.mkdir(target)
if os.listdir(target) == []:
    print >>sys.stderr, "Directory is empty: ", target
    fileName = os.path.join(target, "submissionDocumentation.log")
    f = open(fileName, 'a')
    f.write("No submission documentation added")
    f.close()
    os.chmod(fileName, 488)
else:
    exit(0)
      