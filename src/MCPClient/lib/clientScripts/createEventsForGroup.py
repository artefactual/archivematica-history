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
from optparse import OptionParser
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from databaseFunctions import insertIntoEvents
import databaseInterface             


if __name__ == '__main__':
    """creates events for all files in the group"""
    parser = OptionParser()
    parser.add_option("-i",  "--groupUUID",          action="store", dest="groupUUID", default="")
    parser.add_option("-g",  "--groupType",          action="store", dest="groupType", default="")
    parser.add_option("-t",  "--eventType",        action="store", dest="eventType", default="")
    parser.add_option("-d",  "--eventDateTime",     action="store", dest="eventDateTime", default="")
    parser.add_option("-e",  "--eventDetail",       action="store", dest="eventDetail", default="")
    parser.add_option("-o",  "--eventOutcome",      action="store", dest="eventOutcome", default="")
    parser.add_option("-n",  "--eventOutcomeDetailNote",   action="store", dest="eventOutcomeDetailNote", default="")
    parser.add_option("-u",  "--eventIdentifierUUID",      action="store", dest="eventIdentifierUUID", default="")
   
    
    (opts, args) = parser.parse_args()
    sql = """SELECT fileUUID FROM Files WHERE removedTime = 0 AND %s = '%s';""" % (opts.groupType, opts.groupUUID)
    rows = databaseInterface.queryAllSQL(sql) 
    for row in rows:
        fileUUID = row[0]
        insertIntoEvents(fileUUID=fileUUID, \
                     eventIdentifierUUID=opts.eventIdentifierUUID, \
                     eventType=opts.eventType, \
                     eventDateTime=opts.eventDateTime, \
                     eventDetail=opts.eventDetail, \
                     eventOutcome=opts.eventOutcome, \
                     eventOutcomeDetailNote=opts.eventOutcomeDetailNote)  
