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

import databaseInterface
from linkTaskManager import linkTaskManager
from taskStandard import taskStandard

class linkTaskManagerDirectory:
    def __init__(self, pk, unit):
        self.tasks = []
        self.pk = pk
        sql = """SELECT * FROM StandardTasksConfigs where pk = """ + pk.__str__() 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            #pk = row[0] 
            filterFileEnd = row[1]
            filterFileStart = row[2]
            filterSubDir = row[3]
            self.requiresOutputLock = row[4]
            reloadFileList = row[5]
            standardOutputFile = row[6]
            standardErrorFile = row[7]
            execute = row[8]
            arguments = row[9]
            row = c.fetchone()
        sqlLock.release()
        
        if reloadFileList:
            unit.reloadFileList()