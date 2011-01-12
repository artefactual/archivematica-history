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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import sys
import lxml.etree as etree
import os, glob
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier
from archivematicaFunctions import appendEventToFile


#etree.Element("root", interesting="totally")
#SubElement(root, "child").text = "Child 1"

if __name__ == '__main__':
    eIDValue = sys.argv[1]
    date = sys.argv[2]
    version = sys.argv[3]
    program = sys.argv[4]
    target = sys.argv[5] 
   
    eventDetailText = "program=\"" + program + "\"; version=\"" + version + "\""   
    eventOutcome = createOutcomeInformation(eventOutcomeText="Pass")
    event = createEvent( eIDValue, "fixity check", eventDateTime=date, eventDetailText=eventDetailText, eOutcomeInformation=eventOutcome)
    #print >>sys.stderr, etree.tostring(event, pretty_print=True)
    
    #for every fileMeta file
    for infile in glob.glob( os.path.join(target + "logs/fileMeta/", '*.xml') ): 
        #append the event
        infile = os.path.basename(infile)
        #print >>sys.stderr, infile
        fileUUID = infile[:infile.rfind('.')]
        appendEventToFile(target + "logs/", fileUUID, event)
        

