#!/usr/bin/python

import re
import MySQLdb
import math
import sys
import os
from executeOrRun import executeOrRun
#from premisXMLlinker import xmlNormalize 
LowerEndMainGroupMax = -10

database=MySQLdb.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
commandObjects = {}
groupObjects = {}
commandLinkerObjects = {}
onSuccess=None #pointer to a function to call once a command completes successfully

#this script is passed fileIn, uuid
fileIn = sys.argv[1]
#fileUUID = sys.argv[2]
#accesspath = sys.argv[3]
#xmlStuff = sys.argv[4] #yes/no
#edate = ""
#eid = ""
#objectsPath = ""
#logsPath = ""
#if xmlStuff == "yes":
#    edate = sys.argv[5]
#    eid = sys.argv[6]
#    objectsPath = sys.argv[7]
#    logsPath = sys.argv[8]    



#get file name and extension
s = fileIn
#get indexes for python string array
#index of next char after last /
x1 = s.rfind('/')+1
#index of last .
x2 = s.rfind('.')
#index of next char after last .
x2mod = x2+1
#length of s
sLen = len(s)

if x2 < x1:
    x2mod = 0

fileTitle = s[x1:x2]
fileExtension = s[x2mod:sLen]
fileDirectory = s[:x1]
fileFullName = fileDirectory + fileTitle + "." + fileExtension

def onceExtracted(command):
    extractedFiles = []
    print "TODO - Metadata regarding removal of extracted archive"
    os.remove(command.replacementDic["%inputFile%"])
    for w in os.walk(command.replacementDic["%outputDirectory%"]):
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

onSuccess = onceExtracted

def identifyCommands(fileName):
    """Identify file type(s)"""
    ret = []
    
    RarExtensions = ['.part01.rar', '.r01', '.rar']
    for extension in RarExtensions:
        if fileName.lower().endswith(extension.lower()):
            #sql find the file type,
            c=database.cursor()
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
            c=database.cursor()
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

class Command:
    def __init__(self, commandID):
        self.pk = commandID
        self.exitCode=None
        c=database.cursor()
        sql = """SELECT CT.type, C.verificationCommand, C.command, C.description
        FROM Commands AS C
        JOIN CommandTypes AS CT ON C.commandType = CT.pk
        WHERE C.pk = """ + commandID + """
        ;"""
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            self.type, \
            self.verificationCommand, \
            self.command, \
            self.description = \
            row
            row = c.fetchone()
        if self.verificationCommand:
            self.verificationCommand = Command(self.verificationCommand)
    
    def __str__(self):
        return "[COMMAND]\n" + \
        "PK: " + self.pk.__str__() + "\n" + \
        "Type: " + self.type.__str__() + "\n" + \
        "verificationCommand: " + self.verificationCommand.__str__() + "\n" + \
        "command: " + self.command.__str__() + "\n" + \
        "description: " + self.description.__str__()
    
    def execute(self):
        
        print self.__str__()
        
        #Do a dictionary replacement.
        #Replace replacement strings
        self.replacementDic = { \
        "%inputFile%": fileFullName, \
        "%outputDirectory%": fileFullName + "TODO-DATE", \
        }
        
        #for each key replace all instances of the key in the command string
        for key in self.replacementDic.iterkeys():
            self.command = self.command.replace ( key, self.replacementDic[key] )        
        print self.__str__()
        
        self.exitCode, self.stdOut, self.stdError = executeOrRun(self.type, self.command)      
        
        #If unsuccesful
        if self.exitCode:
            print >>sys.stderr, self.__str__()
            print >>sys.stderr, self.stdOut
            print >>sys.stderr, self.stdError
        
        else:
            if onSuccess:
                onSuccess(self)
        
        xmlStuff = False
        if xmlStuff:
            xmlNormalize(outputFileUUID, \
                         fileDirectory + outputFileUUID + fileTitle + "." + preservationFormat[0].lower(), \
                         preservationConversionCommand[index], \
                         fileUUID, \
                         objectsPath, \
                         eid, \
                         edate, \
                         logsPath, \
                         ) #    {normalized; not normalized}
        return self.exitCode

class CommandLinker:
    def __init__(self, commandLinker):
        self.pk, self.command, self.group = commandLinker
        if self.command in commandObjects:
            self.commandObject = commandObjects[command]
        else:
            co =Command(self.command.__str__())
            self.commandObject = co
            commandObjects[self.command] = co
        
        if self.group in groupObjects:
            self.groupObject = groupObjects[group]
            groupObjects[group].members.append(self)
        else:
            go =Group(self.group, [self])
            self.groupObject = go
            groupObjects[self.group] = go
        
    def __str__(self):
        return "[Command Linker]\n" + \
        "PK: " + self.pk.__str__() + "\n" + \
        self.commandObject.__str__() 
    
    def execute(self):
        if self.commandObject.exitCode != None:
            print "already ran"
            return self.commandObject.exitCode
        else:
            print "running"
            ret = self.commandObject.execute()
            print "need to update database statistics"
            return ret
        

class Group:
    def __init__(self, pk, members=[]):
        self.pk = pk
        self.members = members
    
    def __str__(self):
        members = ""
        for m in self.members:
            members += m.__str__() + "\n"
        return "[GROUP]\n" + \
        "PK: " + self.pk.__str__() + "\n" + \
        members
        
        
def main(fileName):
    #determin the pk's of the Command Linkers
    cls = identifyCommands(fileName)

    if cls == []:
        print "Nothing to do"
        return 0
    
    #Create the groups and command objects for the Command Linkers
    for c in cls:
        cl = CommandLinker(c)
        pk, commandPK, groupPK = c
        commandLinkerObjects[pk] = cl
    
    #execute
    for g in groupObjects:
        if g > 0 or g < LowerEndMainGroupMax:
            for group in groupObjects[g]:
                for cl in group.members:
                    cl.execute()
    mainGroup = 0
    while True :
        if mainGroup in groupObjects:
            combinedExitCode = 0
            for cl in groupObjects[mainGroup].members:
                cl.execute()
                combinedExitCode += math.fabs(cl.commandObject.exitCode)
            if len(groupObjects[mainGroup].members) > 0 and combinedExitCode == 0:
                break 
        if mainGroup == LowerEndMainGroupMax:
            quit(-1)
        mainGroup = mainGroup - 1 
    
    
    #look for problems
    for g in groupObjects:
        #Groups that require at least one good one.
        if g > 0:
            exitCode=-1
            for cl in groupObjects[g].members:
                if cl.commandObject.exitCode == 0: 
                    exitCode = 0
                    break
            if exit:
                quit(exitCode)
        #group that require all good ones
        if g == mainGroup:
            exitCode=0
            for cl in groupObjects[g].members:
                if cl.commandObject.exitCode != 0: 
                    exitCode = -1
                    break
            if exit:
                quit(exitCode)
    quit(0)
    
    
    c="""
    commands2 = {}
    groups2 = {}
    for command in commands:
        pk, commandPK, groupPK = command
        print "GROUP: ", group
        print "pk:", pk

        if command not in commands2:
            c = Command(command.__str__())
            commands2[command] = c
        if group not in groups2:
            groups2[group]= []
        if pk not in groups2[group]:
            (groups2[group]).append(pk)
        
    for command in commands2:
        print command
        print commands2[command]
    for group in groups2:
        print group
        print groups2[group]
        
    """
    
    
    b="""for command in commands:
        pk, command, group = command
        ec = commands2[command].exitCode
        if ec:
            write ec to db.--
    """

    a="""Class commands, id
        dic, gouping pointer to command class object.
        dic, based on id (no duplicates) of command class objects
    
    for every Command in the dictionary
        run the command.
        for every file in the extracted directory (and sub directories):
            fileAddedToSIP
            main() # on the just extracted directory
        store the exit code in the command object
        
    dic, exit code grouping.
    for each item in the grouping dictionary
        if grouping in exit code grouping.
            UPDATE it.
        else
            create it.
            
    compute exit code base on exit code grouping
    exit"""
    
    
    
if __name__ == '__main__':
    import sys
    filename = sys.argv[1].__str__()
    print filename
    main(filename)

