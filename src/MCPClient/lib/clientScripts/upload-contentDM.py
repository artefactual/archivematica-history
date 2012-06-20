#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
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
# @author Mark Jordan <EMAIL@EMAIL.email>
# @version svn: $Id$

# http://docs.python.org/library/argparse.html#module-argparse
# http://www.doughellmann.com/PyMOTW/argparse/
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='restructure')
    parser.add_argument('--uuid', action="store", dest='uuid', metavar='UUID', help='AIP-UUID')
    parser.add_argument('--dipDir', action="store", dest='dipDir', metavar='dipDir', help='DIP Directory')
    parser.add_argument('--server', action="store", dest='contentdmServer', metavar='server', help='Target CONTENTdm server')
    parser.add_argument('--collection', action="store", dest='targetCollection',
                        metavar='targetCollection', help='Target CONTENTdm Collection')
    parser.add_argument('--ingestFormat', action="store", dest='ingestFormat', metavar='ingestFormat',
                        default='directupload', help='The format of the ingest package, either directupload or projectclient')
    parser.add_argument('--outputDir', action="store", dest='outputDir', metavar='outputDir',
                        help='The destination for the restructured DIPs')

    args = parser.parse_args()
    
    print args
    
