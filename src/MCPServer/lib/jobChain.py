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
from jobChainLink import jobChainLink
#Holds:
#-UNIT
#-Job chain link
#-Job chain description
#
#potentialToHold/getFromDB
#-previous chain links
class jobChain:
    def __init__(self, unit, chainPK):
        self.unit = unit
        self.pk = chainPK
        sql = """SELECT * FROM MicroServiceChains WHERE pk =  """ + chainPK.__str__() 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            #self.pk = row[0]
            self.startingChainLink = row[1]
            self.description = row[2]           
            row = c.fetchone()
        sqlLock.release()
        self.currentLink = jobChainLink(self, self.startingChainLink, unit)
        
    
    def nextChainLink(self, pk):
        
        print "got to do: ", pk
        t = threading.Thread(target=self.nextChainLinkThreaded, args=(pk, ))
        t.start()
    
    def nextChainLinkThreaded(self, pk):
        self.currentLink = jobChainLink(self, pk, self.unit)