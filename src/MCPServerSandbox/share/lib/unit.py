#!/usr/bin/python

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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

class unit:
    #Used to write to file
    #@output - the text to append to the file
    #@fileName - The name of the file to create, or append to.
    #@returns - 0 if ok, non zero if error occured.
    def writeToFile(output, fileName):
        if fileName and output:
            print "writing to: " + fileName
            if fileName.startswith("<^Not allowed to write to file^> "):
                return -1
            try:
                f = open(fileName, 'a')
                f.write(output.__str__())
                f.close()
                os.chmod(fileName, 488)
            except OSError, ose:
                print >>sys.stderr, "output Error", ose
                return -2
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
                return -3
        else:
            print "No output, or file specified"
        return 0