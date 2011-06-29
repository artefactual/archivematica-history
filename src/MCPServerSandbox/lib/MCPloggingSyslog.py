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

import os
import threading
import syslog
from archivematicaReplacementDics import getSIPUUID

syslogLoggingLock = threading.Lock()
syslog.openlog("Archivematica MCP",syslog.LOG_PID)
separator = ", "


def runSyslog( log ):
    syslogLoggingLock.acquire()
    syslog.syslog( log )
    syslogLoggingLock.release()

def logTaskCreatedSyslog(task, replacementDic):
    taskUUID = task.UUID.__str__()
    jobUUID = task.job.UUID.__str__()
    fileUUID = replacementDic["%fileUUID%"].__str__()
    taskexec = task.execute
    arguments = task.arguments
    fileName = os.path.basename(replacementDic["%relativeLocation%"])
   
    runSyslog("Task Created: "  + taskUUID + separator + jobUUID + separator + fileUUID + separator + fileName + separator + taskexec + separator + arguments )

def logTaskAssignedSyslog(task, client):
    taskUUID = task.UUID.__str__()
    client = client.clientName   

    runSyslog("Task Assigned: " + taskUUID + separator + client)


def logTaskCompletedSyslog(task, retValue):
    taskUUID = task.UUID.__str__()
    exitCode = retValue.__str__()
    
    runSyslog("Task Completed: " + taskUUID + separator + exitCode)

def logJobCreatedSyslog(job):
    runSyslog("Job Created: " + job.UUID.__str__() + separator + job.directory + separator + getSIPUUID(job.directory + "/") )


def logJobStepCompletedSyslog(job):
    runSyslog("Job Step Complete: " + job.UUID.__str__() + separator + job.step )


