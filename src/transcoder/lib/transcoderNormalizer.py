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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


import sys
import os
from transcoder import main
from transcoder import setFileIn
from executeOrRun import executeOrRun
from optparse import OptionParser
import transcoder
import uuid
from premisXMLlinker import xmlNormalize 
from getPronomsFromPremis import getPronomsFromPremis

print "Todo: change outputFileUUID to task uuid on first run"
global replacementDic
global opts
global outputFileUUID

def inAccessFormat():
    ex=["CSS", "CSV", "HTML", "TXT", "XML", "XSL", \
        "MP3", "PDF", "JPG", "MPG"]
    return transcoder.fileExtension.__str__().upper() in ex

def inPreservationFormat():
    ex=["CSS", "CSV", "HTML", "TXT", "XML", "XSL", \
        "JP2", "PNG", \
        "svg", "WAV", "TIF", "PDF", "ODP", "TIF", "MXF", "ODT", "ODS", "PST", "AI" ]
    return transcoder.fileExtension.__str__().upper() in ex

def onceNormalized(command):
    transcodedFiles = []
    
    if not command.outputLocation:
        command.outputLocation = ""
    elif os.path.isfile(command.outputLocation):
        transcodedFiles.append(command.outputLocation)
    elif os.path.isdir(command.outputLocation):        
        for w in os.walk(command.outputLocation):
            path, directories, files = w
            for p in files:
                p = os.path.join(path, p)
                if os.path.isfile(p):
                    transcodedFiles.append(p)
    elif command.outputLocation:
        print >>sys.stderr, command
        print >>sys.stderr, "Error - output file does not exist [" + command.outputLocation + "]"
        command.exitCode = -2
             
    for ef in transcodedFiles:
        global outputFileUUID
        global replacementDic
        global opts
        if opts.commandClassifications == "normalize":
            xmlNormalize(outputFileUUID, \
                     ef, \
                     command.eventDetailCommand.stdOut, \
                     opts.fileUUID, \
                     opts.objectsDirectory, \
                     opts.taskUUID, \
                     opts.date, \
                     opts.logsDirectory, \
                     ) #    {normalized; not normalized}
            outputFileUUID = uuid.uuid4().__str__() 
            replacementDic["%postfix%"] = "-" + outputFileUUID             

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    c=transcoder.database.cursor()
    if transcoder.fileExtension:
        sql = """SELECT CR.pk, CR.command, CR.GroupMember 
        FROM CommandRelationships AS CR 
        JOIN FileIDs ON CR.fileID=FileIDs.pk 
        JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk
        JOIN FileIDsByExtension AS FIBE  ON FileIDs.pk = FIBE.FileIDs 
        WHERE FIBE.Extension = '""" + transcoder.fileExtension.__str__() + """'  
        AND CommandClassifications.classification = '""" + opts.commandClassifications +"""';"""
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            ret.append(row)
            row = c.fetchone()  
    
    premisFile = opts.logsDirectory + "fileMeta/" + opts.fileUUID + ".xml"
    for pronomID in getPronomsFromPremis(premisFile):
        sql = """SELECT CR.pk, CR.command, CR.GroupMember 
        FROM CommandRelationships AS CR 
        JOIN FileIDs ON CR.fileID=FileIDs.pk 
        JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk
        JOIN FileIDsByPronom AS FIBP  ON FileIDs.pk = FIBP.FileIDs 
        WHERE FIBP.FileID = '""" + pronomID.__str__() + """'  
        AND CommandClassifications.classification = '""" + opts.commandClassifications +"""';"""
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            ret.append(row)
            row = c.fetchone()         
     
    if not len(ret):
        if opts.commandClassifications == "normalize":
            if inPreservationFormat():
                print "Already in preservation format."
            else:
                print >>sys.stderr, "Unable to verify archival readiness."
                exit(7)
        
        elif opts.commandClassifications == "access":
            sql = """SELECT CR.pk, CR.command, CR.GroupMember
            FROM CommandRelationships AS CR
            JOIN Commands AS C ON CR.command = C.pk 
            WHERE C.description = 'Copying File.';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                cl = transcoder.CommandLinker(row)
                copyExitCode = cl.execute()
                if copyExitCode:
                    exit(copyExitCode)
                row = c.fetchone()  
            if inAccessFormat():
                print "Already in access format."
                exit(0)
            else:
                print >>sys.stderr, "Unable to verify access readiness."
                exit(7)
    return ret

if __name__ == '__main__':
    global opts
    global replacementDic
    global outputFileUUID
    outputFileUUID = uuid.uuid4().__str__()
    parser = OptionParser()
    #--inputFile "%relativeLocation%" --commandClassifications "normalize" --fileUUID "%fileUUID%" --taskUUID "%taskUUID%" --objectsDirectory "%SIPObjectsDirectory%" --logsDirectory "%SIPLogsDirectory%" --date "%date%"
    parser.add_option("-f",  "--inputFile",          action="store", dest="inputFile", default="")
    parser.add_option("-c",  "--commandClassifications",  action="store", dest="commandClassifications", default="")
    parser.add_option("-i",  "--fileUUID",           action="store", dest="fileUUID", default="")
    parser.add_option("-t",  "--taskUUID",           action="store", dest="taskUUID", default="")
    parser.add_option("-o",  "--objectsDirectory",   action="store", dest="objectsDirectory", default="")
    parser.add_option("-l",  "--logsDirectory",      action="store", dest="logsDirectory", default="")
    parser.add_option("-a",  "--accessDirectory",    action="store", dest="accessDirectory", default="")
    parser.add_option("-d",  "--date",   action="store", dest="date", default="")
    
    
    (opts, args) = parser.parse_args()
    
    filename = opts.inputFile
    setFileIn(fileIn=filename)
    print "Operating on file: ", filename
    print "Using " + opts.commandClassifications + " command classifications"
    
    prefix = ""
    postfix = ""
    outputDirectory = ""
    if opts.commandClassifications == "normalize":
        postfix = "-" + opts.taskUUID
        outputDirectory = transcoder.fileDirectory 
    elif opts.commandClassifications == "access":
        prefix = opts.fileUUID + "-"
        outputDirectory = opts.accessDirectory
    else:
        print >>sys.stderr, "Unsupported command classification."
        exit(2)
    
    replacementDic = { \
        "%inputFile%": transcoder.fileFullName, \
        "%outputDirectory%": outputDirectory, \
        "%fileExtension%": transcoder.fileExtension, \
        "%fileFullName%": transcoder.fileFullName, \
        "%preservationFileDirectory%": transcoder.fileDirectory, \
        "%fileDirectory%": transcoder.fileDirectory,\
        "%fileTitle%": transcoder.fileTitle, \
        "%fileName%":  transcoder.fileTitle, \
        "%prefix%": prefix,
        "%postfix%": postfix
        }
    
    
    transcoder.onSuccess = onceNormalized
    transcoder.identifyCommands = identifyCommands
    transcoder.replacementDic = replacementDic
    main(filename)

