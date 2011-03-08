#!/usr/bin/python

import sys
import os
from transcoder import main
from executeOrRun import executeOrRun
import transcoder
#from premisXMLlinker import xmlNormalize 

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
        "%postfix%": "UUID"
        
        }

def onceNormalized(command):
    extractedFiles = []
    
    if os.path.isfile(command.outputLocation):
        extractedFiles.append(command.outputLocation)
    elif os.path.isdir(command.outputLocation):        
        for w in os.walk(command.outputLocation):
            path, directories, files = w
            for p in files:
                p = os.path.join(path, p)
                print "path: ", p
                if os.path.isfile(p):
                    extractedFiles.append(p)
    elif command.outputLocation != None:
        print >>sys.stderr, "Error - output file does not exist [" + command.outputLocation + "]"
        command.exitCode = -2
             
    for ef in extractedFiles:
        print "TODO - addFile()"
        
        """xmlNormalize(outputFileUUID, \
                     fileDirectory + outputFileUUID + fileTitle + "." + preservationFormat[0].lower(), \
                     preservationConversionCommand[index], \
                     fileUUID, \
                     objectsPath, \
                     eid, \
                     edate, \
                     logsPath, \
                     ) #    {normalized; not normalized} """
                     

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    
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
    transcoder.onSuccess = onceNormalized
    transcoder.identifyCommands = identifyCommands
    transcoder.replacementDic = replacementDic
    filename = sys.argv[1].__str__()
    print filename
    main(filename)

