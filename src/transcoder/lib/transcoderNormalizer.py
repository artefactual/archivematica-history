#!/usr/bin/python

import sys
import os
from transcoder import main
from transcoder import setFileIn
from executeOrRun import executeOrRun
from optparse import OptionParser
import transcoder
import uuid
from premisXMLlinker import xmlNormalize 

print "Todo: change outputFileUUID to task uuid on first run"
outputFileUUID = uuid.uuid4().__str__()
global replacementDic
global opts
global outputFileUUID

def onceNormalized(command):
    transcodedFiles = []
    
    if os.path.isfile(command.outputLocation):
        transcodedFiles.append(command.outputLocation)
    elif os.path.isdir(command.outputLocation):        
        for w in os.walk(command.outputLocation):
            path, directories, files = w
            for p in files:
                p = os.path.join(path, p)
                print "path: ", p
                if os.path.isfile(p):
                    transcodedFiles.append(p)
    elif command.outputLocation != None:
        print >>sys.stderr, "Error - output file does not exist [" + command.outputLocation + "]"
        command.exitCode = -2
             
    for ef in transcodedFiles:
        print "TODO - addFile()"
        global outputFileUUID
        global replacementDic
        global opts
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
        replacementDic["%postfix%"] = outputFileUUID             

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    print "file extention: ", transcoder.fileExtension.__str__()
    if transcoder.fileExtension:
        c=transcoder.database.cursor()
        sql = """SELECT CR.pk, CR.command, CR.GroupMember 
        FROM CommandRelationships AS CR 
        JOIN FileIDs ON CR.fileID=FileIDs.pk 
        JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk
        JOIN FileIDsByExtension AS FIBE  ON FileIDs.pk = FIBE.FileIDs 
        WHERE FIBE.Extension = '""" + transcoder.fileExtension.__str__() + """'  
        AND CommandClassifications.classification = 'normalize';"""
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            ret.append(row)
            row = c.fetchone()   
    return ret

if __name__ == '__main__':
    global opts
    global replacementDic
    global outputFileUUID
    parser = OptionParser()
    #--inputFile "%relativeLocation%" --commandClassifications "normalize" --fileUUID "%fileUUID%" --taskUUID "%taskUUID%" --objectsDirectory "%SIPObjectsDirectory%" --logsDirectory "%SIPLogsDirectory%" --date "%date%"
    parser.add_option("-f",  "--inputFile",          action="store", dest="inputFile", default="")
    parser.add_option("-c",  "--commandClassifications",  action="store", dest="commandClassifications", default="")
    parser.add_option("-i",  "--fileUUID",           action="store", dest="fileUUID", default="")
    parser.add_option("-t",  "--taskUUID",           action="store", dest="taskUUID", default="")
    parser.add_option("-o",  "--objectsDirectory",   action="store", dest="objectsDirectory", default="")
    parser.add_option("-l",  "--logsDirectory",      action="store", dest="logsDirectory", default="")
    parser.add_option("-d",  "--date",   action="store", dest="date", default="")
    
    
    (opts, args) = parser.parse_args()
    
    filename = opts.inputFile
    setFileIn(fileIn=filename)
    print "Operating on file: ", filename
    
    if opts.taskUUID:
        outputFileUUID = opts.taskUUID 
    
    replacementDic = { \
        "%inputFile%": transcoder.fileFullName, \
        "%outputDirectory%": transcoder.fileDirectory, \
        "%fileExtension%": transcoder.fileExtension, \
        "%fileFullName%": transcoder.fileFullName, \
        "%preservationFileDirectory%": transcoder.fileDirectory, \
        "%fileDirectory%": transcoder.fileDirectory,\
        "%fileTitle%": transcoder.fileTitle, \
        "%fileName%":  transcoder.fileTitle, \
        "%prefix%": "archivematica",
        "%postfix%": outputFileUUID
        }
    
    
    transcoder.onSuccess = onceNormalized
    transcoder.identifyCommands = identifyCommands
    transcoder.replacementDic = replacementDic
    main(filename)

