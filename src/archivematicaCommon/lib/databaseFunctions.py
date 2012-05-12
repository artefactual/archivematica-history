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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import os
import sys
import databaseInterface
import MySQLdb
import uuid
from archivematicaFunctions import unicodeToStr

def escapeForDB(str):
    str = unicodeToStr(str)
    str = MySQLdb.escape_string(str)
    return str

def insertIntoFiles(fileUUID, filePath, enteredSystem=databaseInterface.getUTCDate(), transferUUID="", sipUUID="", use="original"):
    if transferUUID != "" and sipUUID == "":
        databaseInterface.runSQL("""INSERT INTO Files (fileUUID, originalLocation, currentLocation, enteredSystem, fileGrpUse, transferUUID)
        VALUES ( '"""   + fileUUID + databaseInterface.separator \
                        + escapeForDB(filePath) + databaseInterface.separator \
                        + escapeForDB(filePath) + databaseInterface.separator \
                        + enteredSystem + databaseInterface.separator \
                        + use + databaseInterface.separator \
                        + transferUUID + "' )" )
    elif transferUUID == "" and sipUUID != "":
        databaseInterface.runSQL("""INSERT INTO Files (fileUUID, originalLocation, currentLocation, enteredSystem, fileGrpUse, sipUUID)
        VALUES ( '"""   + fileUUID + databaseInterface.separator \
                        + escapeForDB(filePath) + databaseInterface.separator \
                        + escapeForDB(filePath) + databaseInterface.separator \
                        + enteredSystem + databaseInterface.separator \
                        + use + databaseInterface.separator \
                        + sipUUID + "' )" )
    else:
        print >>sys.stderr, "not supported yet - both SIP and transfer UUID's defined (or neither defined)"
        print >>sys.stderr, "SIP UUID:", sipUUID
        print >>sys.stderr, "transferUUID:", transferUUID
        raise Exception("not supported yet - both SIP and transfer UUID's defined (or neither defined)", sipUUID + "-" + transferUUID)

def insertIntoEvents(fileUUID="", eventIdentifierUUID="", eventType="", eventDateTime=databaseInterface.getUTCDate(), eventDetail="", eventOutcome="", eventOutcomeDetailNote=""):
    if eventIdentifierUUID == "":
        eventIdentifierUUID = uuid.uuid4().__str__()
    databaseInterface.runSQL("""INSERT INTO Events (fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcome, eventOutcomeDetailNote)
            VALUES ( '"""   + escapeForDB(fileUUID) + databaseInterface.separator \
                            + escapeForDB(eventIdentifierUUID) + databaseInterface.separator \
                            + escapeForDB(eventType) + databaseInterface.separator \
                            + escapeForDB(eventDateTime) + databaseInterface.separator \
                            + escapeForDB(eventDetail) + databaseInterface.separator \
                            + escapeForDB(eventOutcome) + databaseInterface.separator \
                            + escapeForDB(eventOutcomeDetailNote) + "' )" )

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
        + escapeForDB(fileUUID) + databaseInterface.separator \
        + escapeForDB(fitsXMLString) + "');")

def insertIntoFilesIDs(fileUUID="", formatName="", formatVersion="", formatRegistryName="", formatRegistryKey=""):
    databaseInterface.runSQL("""INSERT INTO FilesIDs
        (fileUUID, formatName, formatVersion, formatRegistryName, formatRegistryKey)
        VALUES ( '""" \
        + escapeForDB(fileUUID) + databaseInterface.separator \
        + escapeForDB(formatName) + databaseInterface.separator \
        + escapeForDB(formatVersion) + databaseInterface.separator \
        + escapeForDB(formatRegistryName) + databaseInterface.separator \
        + escapeForDB(formatRegistryKey) + "');")



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
                    + escapeForDB(fileUUID) + databaseInterface.separator \
                    + escapeForDB(fileName) + databaseInterface.separator \
                    + escapeForDB(taskexec) + databaseInterface.separator \
                    + escapeForDB(arguments) + databaseInterface.separator \
                    + databaseInterface.getUTCDate() + "' )" )

def logTaskAssignedSQL(taskUUID, client, date):
    databaseInterface.runSQL("UPDATE Tasks " + \
    "SET startTime='" + date + "', client='" + client + "' " + \
    "WHERE taskUUID='" + taskUUID + "';" )

def logTaskCompletedSQL(task):
    print "Logging task output to db", task.UUID
    taskUUID = task.UUID.__str__()
    exitCode = task.results["exitCode"].__str__()
    stdOut = task.results["stdOut"]
    stdError = task.results["stdError"]

    databaseInterface.runSQL("UPDATE Tasks " + \
    "SET endTime='" + databaseInterface.getUTCDate() +"', exitCode='" + exitCode +  "', " + \
    "stdOut='" + escapeForDB(stdOut) + "', stdError='" + escapeForDB(stdError) + "' "
    "WHERE taskUUID='" + taskUUID + "'" )


def logJobCreatedSQL(job):
    separator = databaseInterface.getSeparator()
    unitUUID =  job.unit.UUID
    if job.unit.owningUnit != None:
        unitUUID = job.unit.owningUnit.UUID 
    databaseInterface.runSQL("""INSERT INTO Jobs (jobUUID, jobType, directory, SIPUUID, currentStep, unitType, microserviceGroup, createdTime, createdTimeDec, MicroServiceChainLinksPK, subJobOf)
        VALUES ( '""" + job.UUID.__str__() + separator + escapeForDB(job.description) + separator \
        + escapeForDB(job.unit.currentPath) + separator + escapeForDB(unitUUID) + \
        separator + "Executing command(s)" + separator + job.unit.__class__.__name__  + separator + job.microserviceGroup.__str__() + separator + job.createdDate + separator + databaseInterface.getDeciDate("." + job.createdDate.split(".")[-1]) + "', " + job.pk.__str__()  + ", '" + job.subJobOf.__str__() + "' )" )
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

def createSIP(path, UUID=None):
    if UUID == None:
        UUID = uuid.uuid4().__str__()
    print "Creating SIP:", UUID, "-", path
    sql = """INSERT INTO SIPs (sipUUID, currentPath)
        VALUES ('""" + UUID + databaseInterface.separator + escapeForDB(path) + "');"
    databaseInterface.runSQL(sql)
    return UUID

def deUnicode(str):
    if str == None:
        return None
    return unicode(str).encode('utf-8')
