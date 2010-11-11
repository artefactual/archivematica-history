#!/usr/bin/python

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#import xml.etree.cElementTree as etree  
from commands.commands import commandsClass
import xml.etree.ElementTree as etree
import os

class modulesClass():
    #Vars
    requiresUserApproval = False
    descriptionForApproval = ""
    
    #Commands
    exeCommand = None
    verificationCommand = None
    cleanupSuccessfulCommand = None
    cleanupUnsuccessfulCommand = None
    
    #Directories
    watchDirectory = ""
    processingDirectory = ""
    successDirectory = ""
    failureDirectory = ""
    
    def getTagged(self, root, tag):
        ret = []
        for element in root:
            if element.tag == tag:
                ret.append(element)
        if len(ret) != 1 :
            print "error in config file: " + self.fileName
        return ret

    def __init__(self, directory, fileName): 
        self.fileName = fileName
        self.fileName = directory + "/" + fileName
        
        self.type = os.path.basename(fileName).split(".xml")[0] 
        tree = etree.parse( self.fileName )
        root = tree.getroot()
        
        self.requiresUserApproval = self.getTagged(root, "requiresUserApproval")[0].text.lower() == "yes"
        self.descriptionForApproval = self.getTagged(root, "descriptionForApproval")[0].text
        
        directories = self.getTagged(root, "directories")[0]
        self.watchDirectory = self.getTagged(directories, "watchDirectory")[0].text
        self.processingDirectory = self.getTagged(directories, "processingDirectory")[0].text
        self.successDirectory = self.getTagged(directories, "successDirectory")[0].text
        self.failureDirectory = self.getTagged(directories, "failureDirectory")[0].text
        
        commands = self.getTagged(root, "commands")[0]
        self.exeCommand = commandsClass(self.getTagged(self.getTagged(commands, "exeCommand")[0], "command")[0])
        self.verificationCommand = commandsClass(self.getTagged(self.getTagged(commands, "verificationCommand")[0], "command")[0])
        self.cleanupSuccessfulCommand = commandsClass(self.getTagged(self.getTagged(commands, "cleanupSuccessfulCommand")[0], "command")[0])
        self.cleanupUnsuccessfulCommand = commandsClass(self.getTagged(self.getTagged(commands, "cleanupUnsuccessfulCommand")[0], "command")[0])

            
        
    def __str__(self):
        ret = "Description for Approval: " + self.descriptionForApproval +\
         "\nRequires User Approval: " + self.requiresUserApproval.__str__()
        return ret
