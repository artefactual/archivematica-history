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

import databaseInterface
import threading
import uuid
import sys
import time
#select * from MicroServiceChainChoice JOIN MicroServiceChains on chainAvailable = MicroServiceChains.pk;
#| pk | choiceAvailableAtLink | chainAvailable | pk | startingLink | description

from linkTaskManager import linkTaskManager
from taskStandard import taskStandard
import jobChain
import databaseInterface
import lxml.etree as etree
import os
import archivematicaMCP
global choicesAvailableForUnits
choicesAvailableForUnits = {}
choicesAvailableForUnitsLock = threading.Lock()

class linkTaskManagerChoice:
    def __init__(self, jobChainLink, pk, unit):
        self.choices = []
        self.pk = pk
        self.jobChainLink = jobChainLink
        self.UUID = uuid.uuid4().__str__()
        self.unit = unit
        sql = """SELECT chainAvailable, description FROM MicroServiceChainChoice JOIN MicroServiceChains on chainAvailable = MicroServiceChains.pk WHERE choiceAvailableAtLink = """ + jobChainLink.pk.__str__() 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            chainAvailable = row[0] 
            description = row[1]
            self.choices.append((chainAvailable, description))
            row = c.fetchone()
        sqlLock.release()
        
        preConfiguredChain = self.checkForPreconfiguredXML()
        if preConfiguredChain != None:
            time.sleep(archivematicaMCP.config.getint('MCPServer', "waitOnAutoApprove"))
            print "checking for xml file for processing rules. TODO"
            jobChain.jobChain(self.unit, preConfiguredChain)
        else:
            choicesAvailableForUnitsLock.acquire()
            choicesAvailableForUnits[self.jobChainLink.UUID] = self
            choicesAvailableForUnitsLock.release()
            
    def checkForPreconfiguredXML(self):
        ret = None
        xmlFilePath = os.path.join( \
                                        self.unit.currentPath.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1) + "/", \
                                        archivematicaMCP.config.get('MCPServer', "processingXMLFile") \
                                    )
                            
        if os.path.isfile(xmlFilePath):
            # For a list of items with pks: 
            # SELECT TasksConfigs.description, choiceAvailableAtLink, ' ' AS 'SPACE', MicroServiceChains.description, chainAvailable FROM MicroServiceChainChoice Join MicroServiceChains on MicroServiceChainChoice.chainAvailable = MicroServiceChains.pk Join MicroServiceChainLinks on MicroServiceChainLinks.pk = MicroServiceChainChoice.choiceAvailableAtLink Join TasksConfigs on TasksConfigs.pk = MicroServiceChainLinks.currentTask ORDER BY choiceAvailableAtLink desc;
            try:
                tree = etree.parse(xmlFilePath)
                root = tree.getroot()
                for preconfiguredChoice in root.find("preconfiguredChoices"):
                    #if int(preconfiguredChoice.find("appliesTo").text) == self.jobChainLink.pk:
                    if preconfiguredChoice.find("appliesTo").text == self.jobChainLink.description:
                        desiredChoice = preconfiguredChoice.find("goToChain").text
                        sql = """SELECT MicroServiceChains.pk FROM MicroServiceChainChoice Join MicroServiceChains on MicroServiceChainChoice.chainAvailable = MicroServiceChains.pk WHERE MicroServiceChains.description = '%s' AND MicroServiceChainChoice.choiceAvailableAtLink = %s;""" % (desiredChoice, self.jobChainLink.pk.__str__())
                        c, sqlLock = databaseInterface.querySQL(sql) 
                        row = c.fetchone()
                        while row != None:
                            ret = row[0] 
                            row = c.fetchone()
                        sqlLock.release()
                
            except Exception as inst:
                print >>sys.stderr, "Error parsing xml:"
                print >>sys.stderr, type(inst)
                print >>sys.stderr, inst.args 
                     
            
        return ret
    
    def xmlify(self):
        
        ret = etree.Element("choicesAvailableForUnit")
        etree.SubElement(ret, "UUID").text = self.jobChainLink.UUID
        ret.append(self.unit.xmlify())
        choices = etree.SubElement(ret, "choices")
        for chainAvailable, description in self.choices:
            choice = etree.SubElement(choices, "choice")
            etree.SubElement(choice, "chainAvailable").text = chainAvailable.__str__()
            etree.SubElement(choice, "description").text = description
        return ret 
            
        
        
    def proceedWithChoice(self, chain):
        choicesAvailableForUnitsLock.acquire()
        del choicesAvailableForUnits[self.jobChainLink.UUID]
        choicesAvailableForUnitsLock.release()  
        jobChain.jobChain(self.unit, chain)
