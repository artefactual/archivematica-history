#!/usr/bin/python -OO

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

import sys
import threading
from jobChainLink import jobChainLink
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
#Holds:
#-UNIT
#-Job chain link
#-Job chain description
#
#potentialToHold/getFromDB
#-previous chain links
class jobChain:
    def __init__(self, unit, chainPK):
        print "jobChain",  unit, chainPK
        if chainPK == None:
            return None
        self.unit = unit
        self.pk = chainPK
        sql = """SELECT * FROM MicroServiceChains WHERE pk =  """ + chainPK.__str__()
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        if row == None:
            sqlLock.release()
            return None
        while row != None:
            print row
            #self.pk = row[0]
            self.startingChainLink = row[1]
            self.description = row[2]           
            row = c.fetchone()
        sqlLock.release()
        self.currentLink = jobChainLink(self, self.startingChainLink, unit)
        if self.currentLink == None:
            return None
        
    def nextChainLink(self, pk):
        if pk != None:
            t = threading.Thread(target=self.nextChainLinkThreaded, args=(pk, ))
            t.daemon = True
            t.start()
        else:
            print "Done with SIP:" + self.unit.UUID
    
    def nextChainLinkThreaded(self, pk):
        self.currentLink = jobChainLink(self, pk, self.unit)
        