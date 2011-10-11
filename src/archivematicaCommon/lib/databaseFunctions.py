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
import MySQLdb
import os
import sys
import databaseInterface
import MySQLdb
import uuid

def insertIntoFiles(fileUUID, filePath, enteredSystem=databaseInterface.getUTCDate(), transferUUID="", sipUUID=""):
    if transferUUID != "" and sipUUID == "":
        databaseInterface.runSQL("""INSERT INTO Files (fileUUID, originalLoacation, currentLocation, enteredSystem, transferUUID)
        VALUES ( '"""   + fileUUID + databaseInterface.separator \
                        + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                        + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                        + enteredSystem + databaseInterface.separator \
                        + transferUUID + "' )" )
    elif transferUUID == "" and sipUUID != "":
        databaseInterface.runSQL("""INSERT INTO Files (fileUUID, originalLoacation, currentLocation, enteredSystem, sipUUID)
        VALUES ( '"""   + fileUUID + databaseInterface.separator \
                        + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                        + MySQLdb.escape_string(filePath) + databaseInterface.separator \
                        + enteredSystem + databaseInterface.separator \
                        + sipUUID + "' )" )
    else:
        print >>sys.stderr, "not supported yet - both SIP and transfer UUID's defined (or neither defined)"
        print >>sys.stderr, "SIP UUID:", sipUUID
        print >>sys.stderr, "transferUUID:", transferUUID
        raise Exception("not supported yet - both SIP and transfer UUID's defined (or neither defined)", sipUUID + "-" + transferUUID)

def insertIntoEvents(fileUUID="", eventIdentifierUUID="", eventType="", eventDateTime=databaseInterface.getUTCDate(), eventDetail="", eventOutcome="", eventOutcomeDetailNote=""):  
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

def insertIntoFilesFits(fileUUID="", fitsXMLString=""):
    databaseInterface.runSQL("""INSERT INTO FilesFits
        (fileUUID, FITSxml) 
        VALUES ( '""" \
        + MySQLdb.escape_string(fileUUID) + databaseInterface.separator \
        + MySQLdb.escape_string(fitsXMLString) + "');")

def insertIntoFilesIDs(fileUUID="", formatName="", formatVersion="", formatRegistryName="", formatRegistryKey=""):
    databaseInterface.runSQL("""INSERT INTO FilesIDs
        (fileUUID, formatName, formatVersion, formatRegistryName, formatRegistryKey) 
        VALUES ( '""" \
        + MySQLdb.escape_string(fileUUID) + databaseInterface.separator \
        + MySQLdb.escape_string(formatName) + databaseInterface.separator \
        + MySQLdb.escape_string(formatVersion) + databaseInterface.separator \
        + MySQLdb.escape_string(formatRegistryName) + databaseInterface.separator \
        + MySQLdb.escape_string(formatRegistryKey) + "');")
    
        
    
#user approved?
#client connected/disconnected.

def logTaskCreatedSQL(taskManager, commandReplacementDic, taskUUID, arguments):
    taskUUID = taskUUID
    jobUUID = taskManager.jobChainLink.UUID
    fileUUID = ""
    if "%fileUUID%" in commandReplacementDic:
        fileUUID = commandReplacementDic["%fileUUID%"]
    taskexec = taskManager.execute
    fileName = os.path.basename(os.path.abspath(commandReplacementDic["%relativeLocation%"]))
      
    databaseInterface.runSQL("""INSERT INTO Tasks (taskUUID, jobUUID, fileUUID, fileName, exec, arguments, createdTime)
    VALUES ( '"""   + taskUUID + databaseInterface.separator \
                    + jobUUID + databaseInterface.separator \
                    + MySQLdb.escape_string(fileUUID) + databaseInterface.separator \
                    + MySQLdb.escape_string(fileName) + databaseInterface.separator \
                    + MySQLdb.escape_string(taskexec) + databaseInterface.separator \
                    + MySQLdb.escape_string(arguments) + databaseInterface.separator \
                    + databaseInterface.getUTCDate() + "' )" )

def logTaskAssignedSQL(taskUUID, client, date):   
    databaseInterface.runSQL("UPDATE Tasks " + \
    "SET startTime='" + date + "', client='" + client + "' " + \
    "WHERE taskUUID='" + taskUUID + "'" )

def logTaskCompletedSQL(task):
    print "Logging task output to db", task.UUID
    taskUUID = task.UUID.__str__()
    exitCode = task.results["exitCode"].__str__()
    stdOut = task.results["stdOut"]
    stdError = task.results["stdError"]
    
    databaseInterface.runSQL("UPDATE Tasks " + \
    "SET endTime='" + databaseInterface.getUTCDate() +"', exitCode='" + exitCode +  "', " + \
    "stdOut='" + MySQLdb.escape_string(stdOut) + "', stdError='" + MySQLdb.escape_string(stdError) + "' "
    "WHERE taskUUID='" + taskUUID + "'" )


def logJobCreatedSQL(job):
    separator = databaseInterface.getSeparator()
    databaseInterface.runSQL("""INSERT INTO Jobs (jobUUID, jobType, directory, SIPUUID, currentStep, unitType, microserviceGroup, createdTime, createdTimeDec)
        VALUES ( '""" + job.UUID.__str__() + separator + MySQLdb.escape_string(job.description) + separator \
        + MySQLdb.escape_string(job.unit.currentPath) + separator + MySQLdb.escape_string(job.unit.UUID) + \
        separator + "Executing command(s)" + separator + job.unit.__class__.__name__  + separator + job.microserviceGroup.__str__() + separator + job.createdDate + separator + databaseInterface.getDeciDate("." + job.createdDate.split(".")[-1]) + "' )" )
    #TODO -un hardcode executing exeCommand


def logJobStepCompletedSQL(job):
    databaseInterface.runSQL("""INSERT INTO jobStepCompleted (jobUUID, step, completedTime)
        VALUES ( '""" + job.UUID.__str__() + databaseInterface.separator + job.step + databaseInterface.separator + databaseInterface.getUTCDate() + "' )" )
  
def fileWasRemoved(fileUUID, utcDate=databaseInterface.getUTCDate(), eventDetail = "", eventOutcomeDetailNote = "", eventOutcome=""):
    eventIdentifierUUID = uuid.uuid4().__str__()
    eventType = "file removed"
    eventDateTime = utcDate
    insertIntoEvents(fileUUID=fileUUID, \
                       eventIdentifierUUID=eventIdentifierUUID, \
                       eventType=eventType, \
                       eventDateTime=eventDateTime, \
                       eventDetail=eventDetail, \
                       eventOutcome=eventOutcome, \
                       eventOutcomeDetailNote=eventOutcomeDetailNote)

    
    databaseInterface.runSQL("UPDATE Files " + \
       "SET removedTime='" + utcDate + "', currentLocation=NULL " + \
       "WHERE fileUUID='" + fileUUID + "'" )
        