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
#select * from MicroServiceChainChoice JOIN MicroServiceChains on chainAvailable = MicroServiceChains.pk;
#| pk | choiceAvailableAtLink | chainAvailable | pk | startingLink | description

from linkTaskManager import linkTaskManager
from taskStandard import taskStandard
import jobChain
import databaseInterface
import lxml.etree as etree
import os
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
        
        if False:
            print "checking for xml file for processing rules. TODO"
        else:
            choicesAvailableForUnitsLock.acquire()
            choicesAvailableForUnits[self.UUID] = self
            choicesAvailableForUnitsLock.release()
            
    
    def xmlify(self):
        
        ret = etree.Element("choicesAvailableForUnit")
        etree.SubElement(ret, "UUID").text = self.UUID
        ret.append(self.unit.xmlify())
        choices = etree.SubElement(ret, "choices")
        for chainAvailable, description in self.choices:
            choice = etree.SubElement(choices, "choice")
            etree.SubElement(choice, "chainAvailable").text = chainAvailable.__str__()
            etree.SubElement(choice, "description").text = description
        return ret 
            
        
        
    def proceedWithChoice(self, chain):
        choicesAvailableForUnitsLock.acquire()
        del choicesAvailableForUnits[self.UUID]
        choicesAvailableForUnitsLock.release()  
        jobChain.jobChain(self.unit, chain)
