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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import sys
import lxml.etree as etree
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier
import os
import sys
import string

from datetime import datetime

DetoxDic={}
UUIDsDic={}



def loadDetoxDic():
    detox_fh = open(logsDIR+"filenameCleanup.log", "r")
 
    line = detox_fh.readline()
    while line:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0]
            newfile = detoxfiles[1]
            newfile = string.replace(newfile, "\n", "", 1)
            oldfile = os.path.basename(oldfile)
            DetoxDic[newfile] = oldfile
        line = detox_fh.readline()

def loadFileUUIDsDic():
    FileUUIDs_fh = open(logsDIR+"FileUUIDs.log", "r")
 
    line = FileUUIDs_fh.readline()
    while line:
        detoxfiles = line.split(" -> ",1)
        if len(detoxfiles) > 1 :
            fileUUID = detoxfiles[0]
            fileName = detoxfiles[1]
            fileName = string.replace(fileName, "\n", "", 1)
            UUIDsDic[fileName] = fileUUID
        line = FileUUIDs_fh.readline()

if __name__ == '__main__':
    """This prints the contents for an Archivematica Clamscan Event xml file"""
    eIDValue = sys.argv[1]
    date = sys.argv[2]
    logsDIR = sys.argv[1]

    
    outcome = sys.argv[4]
    expectedOutcome = sys.argv[5]
    version = vers.split("/", 1)[0]
    virusDefs = vers.split("/", 1)[0]
    eventDetailText = "program=\"Clam AV\"; version=\"" + version + "\"; virusDefinitions=\"" + virusDefs + "\""
    eventDetail = etree.Element("eventDetail")
    eventDetail.text = eventDetailText
    
    eventOutcome = None
    if outcome.strip() == expectedOutcome.strip():
        eventOutcome = createOutcomeInformation( eventOutcomeDetailNote = "Pass")
    else:
        eventOutcome = createOutcomeInformation( eventOutcomeDetailNote = "Fail")
    
    event = createEvent( eIDValue, "virus check", eventDateTime=date, eventDetail=eventDetail, eOutcomeInformation=eventOutcome)
    print etree.tostring(event, pretty_print=True)
