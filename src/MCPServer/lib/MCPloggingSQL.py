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

import _mysql
import os
import threading
import MySQLdb
import string
from datetime import datetime
from archivematicaReplacementDics import getSIPUUID

def getUTCDate():    
    """Returns a string of the UTC date & time in ISO format"""
    d = datetime.utcnow()
    return d.isoformat('T')

def getDeciDate(date):
    valid = "." + string.digits
    ret = ""
    for c in date:
        if c in valid:
            ret += c
        #else:
            #ret += replacementChar
    return ret


#sudo apt-get install python-mysqldb
sqlLoggingLock = threading.Lock()
sqlLoggingLock.acquire()
#print "Connecting to Database"
database=_mysql.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
sqlLoggingLock.release()

def runSQL(sql):
    global database
    #found that even though it says it's compiled thread safe, running it multi-threaded crashes it.
    sqlLoggingLock.acquire()
    db = database
    try:
        db.query(sql)
    except MySQLdb.OperationalError, message:  
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=_mysql.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
            sqlLoggingLock.release()
            runSQL(sql)
            return 
    sqlLoggingLock.release()
    return


#user approved?
#client connected/disconnected.

def logTaskCreatedSQL(task, replacementDic):
    taskUUID = task.UUID.__str__()
    jobUUID = task.job.UUID.__str__()
    fileUUID = replacementDic["%fileUUID%"].__str__()
    taskexec = task.execute
    arguments = task.arguments
    fileName = os.path.basename(replacementDic["%relativeLocation%"])
    
    separator = "', '"
    
    runSQL("""INSERT INTO Tasks (taskUUID, jobUUID, fileUUID, fileName, exec, arguments, createdTime)
    VALUES ( '"""   + taskUUID + separator \
                    + jobUUID + separator \
                    + _mysql.escape_string(fileUUID) + separator \
                    + _mysql.escape_string(fileName) + separator \
                    + _mysql.escape_string(taskexec) + separator \
                    + _mysql.escape_string(arguments) + separator \
                    + getUTCDate() + "' )" )

def logTaskAssignedSQL(task, client):
    taskUUID = task.UUID.__str__()
    client = client.clientName
    
    runSQL("UPDATE Tasks " + \
    "SET startTime='" + task.assignedDate + "', client='" + client + "' " + \
    "WHERE taskUUID='" + taskUUID + "'" )

def logTaskCompletedSQL(task, retValue):
    taskUUID = task.UUID.__str__()
    exitCode = retValue.__str__()
    stdOut = task.stdOut
    stdError = task.stdError
    
    runSQL("UPDATE Tasks " + \
    "SET endTime='" + getUTCDate() +"', exitCode='" + exitCode +  "', " + \
    "stdOut='" + _mysql.escape_string(stdOut) + "', stdError='" + _mysql.escape_string(stdError) + "' "
    "WHERE taskUUID='" + taskUUID + "'" )


def logJobCreatedSQL(job):
    separator = "', '"
    runSQL("""INSERT INTO Jobs (jobUUID, jobType, directory, SIPUUID, currentStep, createdTime, createdTimeDec)
    VALUES ( '""" + job.UUID.__str__() + separator + _mysql.escape_string(job.config.type) + separator \
    + _mysql.escape_string(job.directory) + separator + _mysql.escape_string(getSIPUUID(job.directory)) + \
    separator + job.step + separator + job.createdDate + separator + getDeciDate("." + job.createdDate.split(".")[-1]) + "' )" )


def logJobStepCompletedSQL(job):
    separator = "', '"
    runSQL("""INSERT INTO jobStepCompleted (jobUUID, step, completedTime)
    VALUES ( '""" + job.UUID.__str__() + separator + job.step + separator + getUTCDate() + "' )" )
  
def logJobStepChangedSQL(job):
    jobUUUID = job.UUID.__str__()
    
    runSQL("UPDATE Jobs " + \
    "SET currentStep='" + job.step +  "' " + \
    "WHERE jobUUID='" + jobUUUID + "'" )        


    
