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

import _mysql
import os
import threading
from archivematicaReplacementDics import getSIPUUIDFromLog

#sudo apt-get install python-mysqldb
sqlLoggingLock = threading.Lock()
db=_mysql.connect(host="localhost", db="MCP", user="demo", passwd="demo")


def runSQL( sql ):
    sqlLoggingLock.acquire()
    db.query( sql )
    sqlLoggingLock.release()


#user approved?
#client connected/disconnected.

def logTaskCreated(task, replacementDic):
    taskUUID = task.UUID
    jobUUID = task.job.UUID 
    fileUUID = replacementDic["%fileUUID%"]
    taskexec = task.execute
    arguments = task.arguments
    fileName = os.path.basename(replacementDic["%relativeLocation%"])
    
    separator = "', '"
    
    runSQL("""INSERT INTO taskCreated (taskUUID, jobUUID, fileUUID, fileName, exec, arguments)
    VALUES ( '""" + taskUUID.__str__() + separator + jobUUID.__str__() + separator + fileUUID.__str__() + separator + fileName + separator + taskexec + separator + arguments + "' )" )

def logTaskAssigned(task, client):
    taskUUID = task.UUID
    client = client.clientName
    
    separator = "', '"

    runSQL("""INSERT INTO taskAssigned (taskUUID, client)
    VALUES ( '""" + taskUUID.__str__() + separator + client + "' )" )

def logTaskCompleted(task, retValue):
    taskUUID = task.UUID
    exitCode = retValue
    
    separator = "', '"
    
    runSQL("""INSERT INTO taskCompleted (taskUUID, exitCode)
    VALUES ( '""" + taskUUID.__str__() + separator + exitCode.__str__() + "' )" )


def logJobCreated(job):
    separator = "', '"
    runSQL("""INSERT INTO jobCreated (jobUUID, directory, SIPUUID)
    VALUES ( '""" + job.UUID.__str__() + separator + job.directory + separator + getSIPUUIDFromLog(job.directory + "/") + "' )" )


def logJobStepCompleted(job):
    separator = "', '"
    runSQL("""INSERT INTO jobStepCompleted (jobUUID, step)
    VALUES ( '""" + job.UUID.__str__() + separator + job.step + "' )" )

if __name__ == '__main__':
    """Insert test data & print it"""
    taskUUID = uuid.uuid4()
    jobUUID = uuid.uuid4()
    fileUUID = "Test fileUUID"
    taskexec = "Test taskexec"
    arguments = "Test arguments"

    client = "Test client"

    exitCode = 0
    
    separator = "', '"
    
    runSQL("""INSERT INTO taskCreated (taskUUID, jobUUID, fileUUID, exec, arguments)
    VALUES ( '""" + taskUUID.__str__() + separator + jobUUID.__str__() + separator + fileUUID.__str__() + separator + taskexec + separator + arguments + "' )" )

    runSQL("""INSERT INTO taskAssigned (taskUUID, client)
    VALUES ( '""" + taskUUID.__str__() + separator + client + "' )" )

    runSQL("""INSERT INTO taskCompleted (taskUUID, exitCode)
    VALUES ( '""" + taskUUID.__str__() + separator + exitCode.__str__() + "' )" )

    
    runSQL("""SELECT * FROM taskAssigned""")
    r=db.store_result()
    o = r.fetch_row()
    while o:
        print o
        o = r.fetch_row()

    runSQL("""SELECT * FROM taskCreated""")
    r=db.store_result()
    o = r.fetch_row()
    while o:
        print o
        o = r.fetch_row()
        
    runSQL("""SELECT * FROM taskCompleted""")
    r=db.store_result()
    o = r.fetch_row()
    while o:
        print o
        o = r.fetch_row()


    
    


    
