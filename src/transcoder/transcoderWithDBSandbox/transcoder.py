#!/usr/bin/python
import re
import MySQLdb
import math
import sys
import os
from executeOrRun import executeOrRun
LowerEndMainGroupMax = -10


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


database=MySQLdb.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
commandObjects = {}
groupObjects = {}
commandLinkerObjects = {}

global onSusccess
onSuccess=None #pointer to a function to call once a command completes successfully
identifyCommands=None

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
            global onSuccess
            if onSuccess:
                onSuccess(self)
            else:
                print "no onSuccess method"
        
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