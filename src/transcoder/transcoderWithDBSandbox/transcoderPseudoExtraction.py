#!/usr/bin/python

import sys
import os
from transcoder import main
from executeOrRun import executeOrRun
import transcoder
#from premisXMLlinker import xmlNormalize 

replacementDic = { \
        "%inputFile%": transcoder.fileFullName, \
        "%outputDirectory%": transcoder.fileFullName + "TODO-DATE", \
        }

def onceExtracted(command):
    extractedFiles = []
    print "TODO - Metadata regarding removal of extracted archive"
    os.remove(replacementDic["%inputFile%"])
    for w in os.walk(replacementDic["%outputDirectory%"]):
        path, directories, files = w
        for p in files:
            p = os.path.join(path, p)
            print "path: ", p
            if os.path.isfile(p):
                extractedFiles.append(p)
    for ef in extractedFiles:
        print "File Extracted:", ef
        print "TODO - addFile()"
        
        run = sys.argv[0].__str__() + " \"" + ef + "\""
        exitCode, stdOut, stdError = executeOrRun("command", run)              
        print stdOut
        print >>sys.stderr, stdError
        if exitCode != 0 and command.exitCode == 0:
            command.exitCode = exitCode 

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    
    RarExtensions = ['.part01.rar', '.r01', '.rar']
    for extension in RarExtensions:
        if fileName.lower().endswith(extension.lower()):
            #sql find the file type,
            c=transcoder.database.cursor()
            sql = """SELECT CR.pk, CR.command, CR.GroupMember 
            FROM CommandRelationships AS CR 
            JOIN FileIDs ON CR.fileID=FileIDs.pk 
            JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk 
            WHERE FileIDs.description='unrar-nonfreeCompatable' 
            AND CommandClassifications.classification = 'extract';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                ret.append(row)
                row = c.fetchone()
            break
    
    SevenZipExtensions = ['.ARJ', '.CAB', '.CHM', '.CPIO',
                  '.DMG', '.HFS', '.LZH', '.LZMA',
                  '.NSIS', '.UDF', '.WIM', '.XAR',
                  '.Z', '.ZIP', '.GZIP', '.TAR',]
    for extension in SevenZipExtensions:
        if fileName.lower().endswith(extension.lower()):
            c=transcoder.database.cursor()
            sql = """SELECT CR.pk, CR.command, CR.GroupMember 
            FROM CommandRelationships AS CR 
            JOIN FileIDs ON CR.fileID=FileIDs.pk 
            JOIN CommandClassifications ON CR.commandClassification = CommandClassifications.pk 
            WHERE FileIDs.description='7ZipCompatable' 
            AND CommandClassifications.classification = 'extract';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                ret.append(row)
                row = c.fetchone()
            break
    return ret

if __name__ == '__main__':
    transcoder.onSuccess = onceExtracted
    transcoder.identifyCommands = identifyCommands
    transcoder.replacementDic = replacementDic
    filename = sys.argv[1].__str__()
    print filename
    main(filename)

