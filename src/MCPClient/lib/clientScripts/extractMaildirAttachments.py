#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import mailbox
import sys
import os
import uuid
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from externals.extractMaildirAttachments import parse
from fileOperations import addFileToTransfer
from fileOperations import updateSizeAndChecksum

def writeFile(filePath, fileContents):   
    try:
        os.makedirs(os.path.dirname(filePath))
    except:
        pass
    print filePath
    FILE = open(filePath,"w")
    FILE.writelines(fileContents)    
    FILE.close()

def addFile(filePath, transferPath, transferUUID, date, eventDetail = ""): 
    taskUUID = uuid.uuid4().__str__()
    fileUUID = uuid.uuid4().__str__()
    filePathRelativeToSIP = filePath.replace(transferPath, "%transferDirectory%", 1)
    addFileToTransfer(filePathRelativeToSIP, fileUUID, transferUUID, taskUUID, date, sourceType="unpacking", eventDetail=eventDetail)
    updateSizeAndChecksum(fileUUID, filePath, date, uuid.uuid4.__str__())

   
if __name__ == '__main__':
    #http://www.doughellmann.com/PyMOTW/mailbox/
    transferDir = sys.argv[1]
    transferUUID =  sys.argv[2]
    date =  sys.argv[3]
    maildir = transferDir + "objects/Maildir/" 
    outXML = transferDir + "logs/attachmentExtraction.xml"
    import lxml.etree as etree
    #print "Extracting attachments from: " + maildir
    root = etree.Element("ArchivematicaMaildirAttachmentExtractionRecord")
    root.set("directory", maildir) 
    for maildirsub2 in os.listdir(maildir):
        maildirsub = os.path.join(maildir, maildirsub2)
        #print "Extracting attachments from: " + maildirsub
        md = mailbox.Maildir(maildirsub)
        directory = etree.SubElement(root, "subDir")
        directory.set("dir", maildirsub2)
        for item in md.iterkeys():
            #print maildirsub2, item
            fil = md.get_file(item)
            out = parse(fil)
            #print fil
            if len(out['attachments']):
                msg = etree.SubElement(directory, "msg")
                etree.SubElement(msg, "Message-ID").text = out['msgobj']['Message-ID'][1:-1]
                etree.SubElement(msg, "Extracted-from").text = item
                etree.SubElement(msg, "Subject").text = out["subject"] 
                etree.SubElement(msg, "Date").text = out['msgobj']['date']
                etree.SubElement(msg, "To").text = out["to"]
                etree.SubElement(msg, "From").text = out["from"]
                for i in range(len(out['attachments'])):
                    attachment = out['attachments'][i]
                    #attachment = StringIO(file_data) TODO LOG TO FILE
                    attch = etree.SubElement(msg, "attachment")
                    attachment.name = attachment.name[1:-1]
                    etree.SubElement(attch, "name").text = attachment.name
                    etree.SubElement(attch, "content_type").text = attachment.content_type
                    etree.SubElement(attch, "size").text = str(attachment.size)
                    # Dates don't appear to be working. Disabling for the moment - Todo
                    #etree.SubElement(attch, "create_date").text = attachment.create_date
                    #etree.SubElement(attch, "mod_date").text = attachment.mod_date
                    #etree.SubElement(attch, "read_date").text = attachment.read_date
                    
                    filePath = os.path.join(transferDir, "objects/attachments", maildirsub2, "[%s][%s]%s" % (item, out["subject"], attachment.name))
                    writeFile(filePath, \
                             attachment)
                    eventDetail="Unpacked from: " + os.path.join(maildir, maildirsub2, item).replace(transferDir, "%transferDirectory%", 1)
                    addFile(filePath, transferDir, transferUUID, date, eventDetail=eventDetail)
    try:
        os.makedirs(os.path.join(os.path.dirname(maildir), "extracted"))
    except:
        pass
    tree = etree.ElementTree(root)
    tree.write(outXML, pretty_print=True, xml_declaration=True)

                    
