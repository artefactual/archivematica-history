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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

from MCPloggingSQL import *
from MCPloggingSyslog import *

def logTaskCreated(task, replacementDic):
    logTaskCreatedSyslog(task, replacementDic)
    logTaskCreatedSQL(task, replacementDic)

def logTaskAssigned(task, client):
    logTaskAssignedSyslog(task, client)
    logTaskAssignedSQL(task, client)

def logTaskCompleted(task, retValue):
    logTaskCompletedSyslog(task, retValue)
    logTaskCompletedSQL(task, retValue)

def logJobCreated(job):
    logJobCreatedSyslog(job)
    logJobCreatedSQL(job)

def logJobStepCompleted(job):
    logJobStepCompletedSyslog(job)
    logJobStepCompletedSQL(job)

def logJobStepChanged(job):
    logJobStepChangedSQL(job)

    


    
