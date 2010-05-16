#!/usr/bin/python
#
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
# @author Peter Van Garderen <peter@artefactual.com>
# @version svn: $Id$

import os
import uuid
import sys
import xml.etree.cElementTree as etree
import string
from xml.sax.saxutils import quoteattr as xml_quoteattr

DetoxDic={}
amdSec=[]

def loadDetoxDic():
  detox_fh = open(sys.argv[1]+"/filenameCleanup.log", "r")
 
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

def newChild(parent, tag, text=None, tailText=None):
  child = etree.Element(tag)
  parent.append(child)
  child.text = text
  if child.tail:
    child.tail = tailText
  else :
    child.tail = "\n"   
  return child


def createDigiprovMD(uuid, filename) :
  digiprovMD = newChild(amdSec, "digiprovMD")
  digiprovMD.set("ID", os.path.basename(filename) + "-" + uuid)
  mdWrap = newChild(digiprovMD,"mdWrap")
  mdWrap.set("MDTYPE", "PREMIS")
  xmlData = newChild(mdWrap, "xmlData")
  premis = newChild(xmlData, "premis")
  premis.set("xmlns", "info:lc/xmlns/premis-v2")
  premis.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
  premis.set("version", "2.0")
  premis.set("xsi:schemaLocation", "info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd")
  objects = newChild(premis, "object")
  objects.set("xsi:type", "file")
  objectIdentifier = newChild(objects, "objectIdentifier")
  objectIdentifierType = newChild(objectIdentifier, "objectIdentifierType", "UUID")
  objectIdentifierValue = newChild(objectIdentifier, "objectIdentifierValue", uuid)
  if filename in DetoxDic:
    #print DetoxDic[filename] + "\t RENAMED: \t" + filename
    originalName = newChild(objects, "originalName", DetoxDic[filename])

def createFileSec(path, parentBranch, structMapParent):
  pathSTR = path.__str__()
  if pathSTR == "/tmp/" + sys.argv[2] + "/" + sys.argv[3]:
    pathSTR = "objects"
  #pathSTR = string.replace(path.__str__(), "/tmp/" + sys.argv[2] + "/" + sys.argv[3], "objects", 1)
  if pathSTR == "/tmp/" + sys.argv[2]:
    pathSTR = sys.argv[3] + "-" + sys.argv[2]
    structMapParent.set("DMDID", "SIP-description")
  filename = os.path.basename(pathSTR)
  parentBranch.set("ID", filename)
  structMapParent.set("LABEL", filename)
  structMapParent.set("TYPE", "directory")

  for item in os.listdir(path):
    itempath = os.path.join(path, item)
    if os.path.isdir(itempath):
      currentBranch = newChild(parentBranch, "fileGrp")
      currentBranch.set("USE", "directory")
      # structMap directory
      div = newChild(structMapParent, "div")

      createFileSec(os.path.join(path, item), currentBranch, div)    
    elif os.path.isfile(itempath):
      myuuid = uuid.uuid4()
      createDigiprovMD(myuuid.__str__(), itempath)
      fileI = newChild(parentBranch, "file")
      filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
      #filename = replace /tmp/"UUID" with /objects/
      pathSTR = string.replace(path.__str__(),"/tmp/"+ sys.argv[2] + "/" + sys.argv[3], "objects", 1)
      
      fileI.set("ID", "file-" + myuuid.__str__())

      Flocat = newChild(fileI, "Flocat")
      Flocat.set("xlink:href", pathSTR + "/" + filename)
      Flocat.set("locType", "other")
      Flocat.set("otherLocType", "system")

      # structMap file
      div = newChild(structMapParent, "div")
      fptr = newChild(div, "fptr")
      fptr.set("FILEID","file-" + myuuid.__str__())
      
if __name__ == '__main__':

  #cd /tmp/$UUID; 
  opath = os.getcwd()
  os.chdir("/tmp/" + sys.argv[2])
  path = os.getcwd()

  loadDetoxDic()
  #print "Detox dictionary:\t" + DetoxDic.__str__()

  if not os.path.isfile(sys.argv[1]+"/METS.xml"):
    print("System error")

  tree = etree.parse(sys.argv[1]+"/METS.xml")
  root = tree.getroot()

  amdSec = newChild(root, "amdSec")
  structMap = newChild(root, "structMap")
  structMapDiv = newChild(structMap, "div")

  fileSec = etree.Element("fileSec")
  fileSec.text = "\n\t\t"
  fileSec.tail = "\n"
  root.append(fileSec)

  sipFileGrp = etree.Element("fileGrp")
  sipFileGrp.text = "\n\t\t\t"
  sipFileGrp.tail = "\n"
  sipFileGrp.set("ID", sys.argv[2].__str__())
  sipFileGrp.set("USE", "Objects package")
  fileSec.append(sipFileGrp)
	
  createFileSec(path, sipFileGrp, structMapDiv)
  
  tree.write(sys.argv[1]+"/METS.xml")
	
  # Restore original path
  os.chdir(opath)
  
