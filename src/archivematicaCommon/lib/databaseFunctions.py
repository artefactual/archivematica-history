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
import MySQLdb

def insertIntoFiles(fileUUID, filePath, enteredSystem=databaseInterface.getUTCDate(), sipUUID=""):
    databaseInterface.runSQL("""INSERT INTO Files (fileUUID, originalLoacation, currentLocation, enteredSystem, sipUUID)
    VALUES ( '"""   + fileUUID + databaseInterface.separator \
                    + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                    + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                    + enteredSystem + databaseInterface.separator \
                    + sipUUID + "' )" )

def insertIntoEvents(fileUUID="", eventIdentifierUUID="", eventType="", eventDateTime="", eventDetail="", eventOutcome="", eventOutcomeDetailNote=""):  
    databaseInterface.runSQL("""INSERT INTO Events (fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcome, eventOutcomeDetailNote)
            VALUES ( '"""   + fileUUID + databaseInterface.separator \
                            + eventIdentifierUUID + databaseInterface.separator \
                            + MySQLdb.escape_string(eventType) + databaseInterface.separator \
                            + MySQLdb.escape_string(eventDateTime) + databaseInterface.separator \
                            + MySQLdb.escape_string(eventDetail) + databaseInterface.separator \
                            + MySQLdb.escape_string(eventOutcome) + databaseInterface.separator \
                            + MySQLdb.escape_string(eventOutcomeDetailNote) + "' )" )
    
def insertIntoDerivations(sourceFileUUID="", derivedFileUUID="", relatedEventUUID=""):
    databaseInterface.runSQL("""INSERT INTO Derivations
        (sourceFileUUID, derivedFileUUID, relatedEventUUID) 
        VALUES ( '""" \
        + sourceFileUUID + databaseInterface.separator \
        + derivedFileUUID + databaseInterface.separator \
        + relatedEventUUID + "');")

#user approved?
#client connected/disconnected.

def logTaskCreatedSQL(task, replacementDic):
    taskUUID = task.UUID.__str__()
    jobUUID = task.job.UUID.__str__()
    fileUUID = replacementDic["%fileUUID%"].__str__()
    taskexec = task.execute
    arguments = task.arguments
    fileName = os.path.basename(replacementDic["%relativeLocation%"])
    
        
    runSQL("""INSERT INTO Tasks (taskUUID, jobUUID, fileUUID, fileName, exec, arguments, createdTime)
    VALUES ( '"""   + taskUUID + databaseInterface.separator \
                    + jobUUID + databaseInterface.separator \
                    + _mysql.escape_string(fileUUID) + databaseInterface.separator \
                    + _mysql.escape_string(fileName) + databaseInterface.separator \
                    + _mysql.escape_string(taskexec) + databaseInterface.separator \
                    + _mysql.escape_string(arguments) + databaseInterface.separator \
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
        runSQL("""INSERT INTO Jobs (jobUUID, jobType, directory, SIPUUID, currentStep, createdTime, createdTimeDec)
    VALUES ( '""" + job.UUID.__str__() + databaseInterface.separator + _mysql.escape_string(job.config.type) + databaseInterface.separator \
    + _mysql.escape_string(job.directory) + databaseInterface.separator + _mysql.escape_string(getSIPUUID(job.directory)) + \
    databaseInterface.separator + job.step + databaseInterface.separator + job.createdDate + databaseInterface.separator + getDeciDate("." + job.createdDate.split(".")[-1]) + "' )" )


def logJobStepCompletedSQL(job):
        runSQL("""INSERT INTO jobStepCompleted (jobUUID, step, completedTime)
    VALUES ( '""" + job.UUID.__str__() + databaseInterface.separator + job.step + databaseInterface.separator + getUTCDate() + "' )" )
  
def logJobStepChangedSQL(job):
    jobUUUID = job.UUID.__str__()
    
    runSQL("UPDATE Jobs " + \
    "SET currentStep='" + job.step +  "' " + \
    "WHERE jobUUID='" + jobUUUID + "'" )        