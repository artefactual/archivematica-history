#!/usr/bin/python

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# --- This is the MCP (master control program) ---
# The intention of this program is to provide a cetralized automated distributed system for performing an arbitrary set of tasks on a directory.
# Distributed in that the work can be performed on more than one physical computer symultaineously.
# Centralized in that there is one centre point for configuring flow through the system.
# Automated in that the tasks performed will be based on the config files and istantiated for each of the targets.
#
# It loads configurations from the XML files.
# These files contain:
# -The associated watch directory
# -A set of commands to run on the files within that directory.
# -The place to move the directory to once it has been processed.
#
# When a directory is placed within a a watch directory, it generates an event.
# The event creates an associated Job.
# The job is an instance of one of the config files (depending on which watch directory geneated the event).
# The job will have a number of steps, for each of the commands.
# The commands will be istanciated into tasks for each of the files within the watch directory of the event, or just one task for the directory (depending on the config).


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


