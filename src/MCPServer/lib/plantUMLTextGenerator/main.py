#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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
# @subpackage MCPServer-plantUMLTextGenerator
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface

def jobChainLinkExitCodesTextGet(exitCode, nextMicroServiceChainLink, exitMessage):
    print """ if "exitCodeIs %s" then""" % (exitCode.__str__())
    a= """-->[true] "Some Activity"
              --> "Another activity"
              -right-> (*)
            else
              ->[false] "Something else"
              -->[Ending process] (*)
            endif"""

def jobChainLinkTextGet(leadIn, pk, label = ""):
    sql = """SELECT MicroServiceChainLinks.currentTask, MicroServiceChainLinks.defaultNextChainLink, TasksConfigs.taskType, TasksConfigs.taskTypePKReference, TasksConfigs.description, MicroServiceChainLinks.reloadFileList, Sounds.fileLocation, MicroServiceChainLinks.defaultExitMessage, MicroServiceChainLinks.microserviceGroup FROM MicroServiceChainLinks LEFT OUTER JOIN Sounds ON MicroServiceChainLinks.defaultPlaySound = Sounds.pk JOIN TasksConfigs on MicroServiceChainLinks.currentTask = TasksConfigs.pk WHERE MicroServiceChainLinks.pk = '%s';""" % (pk.__str__())
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        currentTask = row[0]
        defaultNextChainLink = row[1]
        taskType = row[2]
        taskTypePKReference = row[3]
        description = row[4]
        reloadFileList = row[5]
        defaultSoundFile = row[6]
        defaultExitMessage = row[7]
        microserviceGroup = row[8]

        leadOut = description
        if label != "":
            print ("%s -->[%s] %s") % (leadIn, label, leadOut)
        else:
            print ("%s --> %s") % (leadIn, leadOut)

        sql = """SELECT exitCode, nextMicroServiceChainLink, exitMessage FROM MicroServiceChainLinksExitCodes WHERE microServiceChainLink = '%s';""" % (pk.__str__())
        rows2 = databaseInterface.queryAllSQL(sql)
        for row2 in rows2:
            exitCode = row2[0]
            nextMicroServiceChainLink = row2[1]
            exitMessage = row2[2]
        if defaultNextChainLink:
            print """ if "exitCodeIs Unhandled" then """
            jobChainLinkTextGet("", defaultNextChainLink, label="true")
            print """endif"""


def jobChainTextGet(leadIn, pk):
    sql = """SELECT startingLink, description FROM MicroServiceChains WHERE pk = '%s';""" % (pk.__str__())
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        startingLink = row[0]
        description = row[1]
        leadOut = description + " \"MicroServiceChain\""
        print ("%s --> %s") % (leadIn, leadOut)
        jobChainLinkTextGet(leadOut, startingLink)

if __name__ == '__main__':
    sql = """SELECT watchedDirectoryPath, chain, expectedType FROM WatchedDirectories;"""
    rows = databaseInterface.queryAllSQL(sql)
    i = 1
    for row in rows:
        watchedDirectoryPath = row[0]
        chain = row[1]
        expectedType = row[2]
        print "@startuml", "img/" + i.__str__() + ".png" #img/activity_img10.png
        print "title " + watchedDirectoryPath
        #print "(*) --> " "First activity"
        jobChainTextGet("(*)[" + watchedDirectoryPath + "]" , chain)
        # --> (*)
        print "@enduml"
        i+=1
