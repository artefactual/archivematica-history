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
from SimpleXMLRPCServer import SimpleXMLRPCServer
import archivematicaMCP
from linkTaskManagerChoice import choicesAvailableForUnits
import lxml.etree as etree

def startXMLRPCServer():
    server = SimpleXMLRPCServer( (archivematicaMCP.config.get('MCPServer', 'MCPArchivematicaXMLClients'), archivematicaMCP.config.getint('MCPServer', "MCPArchivematicaXMLPort")))
    server.register_function(getJobsAwaitingApproval)
    server.register_function(approveJob)
    server.serve_forever()
    
def getJobsAwaitingApproval():
    ret = etree.Element("choicesAvailableForUnits")
    for UUID, choice in choicesAvailableForUnits.items():
        ret.append(choice.xmlify())
    return etree.tostring(ret, pretty_print=True)


def approveJob(jobUUID, chain):
    print "approving: ", jobUUID, chain
    if jobUUID in choicesAvailableForUnits:
        choicesAvailableForUnits[jobUUID].proceedWithChoice(chain)
    return "approving: ", jobUUID, chain

    
