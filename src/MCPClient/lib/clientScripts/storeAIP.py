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
import os
import stat
import shutil
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from executeOrRunSubProcess import executeOrRun 

printSubProcessOutput=True

AIPsStore = sys.argv[1]
AIP = sys.argv[2]
SIPUUID = sys.argv[3]
HTMLFilePath = sys.argv[4]
SIPNAME = sys.argv[5]
SIPDATE = sys.argv[6]

#Get the UUID quads
uuidQuads = []
SIPUUIDStripped = SIPUUID.replace("-","")
uuidQuads.append(SIPUUIDStripped[:4])
uuidQuads.append(SIPUUIDStripped[4:7])
uuidQuads.append(SIPUUIDStripped[8:12])
uuidQuads.append(SIPUUIDStripped[12:16])
uuidQuads.append(SIPUUIDStripped[16:20])
uuidQuads.append(SIPUUIDStripped[20:24])
uuidQuads.append(SIPUUIDStripped[24:28])
uuidQuads.append(SIPUUIDStripped[28:32])

AIPsStoreWithQuads = AIPsStore
mode= stat.S_IWUSR + stat.S_IRUSR + stat.S_IXUSR + stat.S_IRGRP + stat.S_IXGRP + stat.S_IXOTH + stat.S_IROTH
for quad in uuidQuads:
    AIPsStoreWithQuads = AIPsStoreWithQuads + quad + "/"
    if not os.path.isdir(AIPsStoreWithQuads):
        os.mkdir(AIPsStoreWithQuads, mode)
        #mode isn't working on the mkdir
        os.chmod(AIPsStoreWithQuads, mode)

storeLocation=os.path.join(AIPsStoreWithQuads, os.path.basename(os.path.abspath(AIP)))

#Store the AIP
shutil.move(AIP, storeLocation)

#Extract the AIP
extractDirectory = "/tmp/" + SIPUUID + "/"
os.makedirs(extractDirectory)
#
command = "7z x -bd -o\"" + extractDirectory + "\" \"" + storeLocation + "\"" 
ret = executeOrRun("command", command, printing=printSubProcessOutput)
exitCode, stdOut, stdErr = ret
if exitCode != 0:
    print >>sys.stderr, "Error extracting"
    quit(1)

bag = extractDirectory + SIPNAME + "-" + SIPUUID + "/"
verificationCommands = []
verificationCommands.append("/usr/share/bagit/bin/bag verifyvalid \"" + bag + "\"")
verificationCommands.append("/usr/share/bagit/bin/bag checkpayloadoxum \"" + bag + "\"")
verificationCommands.append("/usr/share/bagit/bin/bag verifycomplete \"" + bag + "\"")
verificationCommands.append("/usr/share/bagit/bin/bag verifypayloadmanifests \"" + bag + "\"")
verificationCommands.append("/usr/share/bagit/bin/bag verifytagmanifests \"" + bag + "\"")
exitCode = 0
for command in verificationCommands:
    ret = executeOrRun("command", command, printing=printSubProcessOutput)
    exit, stdOut, stdErr = ret
    if exit != 0:
        print >>sys.stderr, "Failed test: ", command
        exitCode=1
    else:
        print >>sys.stderr, "Passed test: ", command
        
#cleanup    
shutil.rmtree(extractDirectory)  

#write to html file
if exitCode == 0:
    link = storeLocation.replace(AIPsStore, "AIPsStore/")
    import lxml.etree as etree
    if os.path.isfile(HTMLFilePath):
        tree = etree.parse(HTMLFilePath)
        body = tree.find("body")

    else:
        root = etree.Element("html")
        head = etree.SubElement(root, "head")
        body = etree.SubElement(root, "body")
        body.tail = "\n"
        tree = etree.ElementTree(root)

    # Calculate position
    position = 0
    for item in body.findall("div"):
      name = item.find('p[@class="name"]/a').text
      if SIPNAME < name:
        break
      position = position + 1

    # Create HTML div object
    div = etree.Element("div")
    div.tail = "\n"

    # SIP name
    sip_name = etree.SubElement(div, "p")
    sip_name.set("class", "name")
    sip_name_link = etree.SubElement(sip_name, "a")
    sip_name_link.text = SIPNAME
    sip_name_link.set("href", link)

    # SIP UUID
    sip_uuid = etree.SubElement(div, "p")
    sip_uuid.set("class", "uuid")
    sip_uuid.text = SIPUUID

    # SIP date
    sip_uuid = etree.SubElement(div, "p")
    sip_uuid.set("class", "date")
    sip_uuid.text = SIPDATE

    # Insert div
    body.insert(position, div)

    # Write HTML
    tree.write(HTMLFilePath)
    os.chmod(HTMLFilePath, mode)

quit(exitCode)
