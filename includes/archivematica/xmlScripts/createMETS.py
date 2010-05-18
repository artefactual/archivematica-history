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
from datetime import datetime

DetoxDic={}
UUIDsDic={}
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

def loadFileUUIDsDic():
  FileUUIDs_fh = open(sys.argv[1]+"/FileUUIDs.log", "r")
 
  line = FileUUIDs_fh.readline()
  while line:
    detoxfiles = line.split(" -> ",1)
    if len(detoxfiles) > 1 :
      fileUUID = detoxfiles[0]
      fileName = detoxfiles[1]
      fileName = string.replace(fileName, "\n", "", 1)
      UUIDsDic[fileName] = fileUUID
    line = FileUUIDs_fh.readline()


def newChild(parent, tag, text=None, tailText=None):
  child = etree.Element(tag)
  parent.append(child)
  child.text = text
  if not parent.text:
    parent.text = "\n"
  if tailText:
    child.tail = tailText
  else :
    child.tail = "\n"   
  return child


def createDigiprovMD(uuid, filename) :
  digiprovMD = newChild(amdSec, "digiprovMD")
  digiprovMD.set("ID", "digiprov" + "-" + uuid)
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

  #Load Fits
  mdWrap = newChild(digiprovMD,"mdWrap")
  mdWrap.set("MDTYPE", "FITS")
  xmlData = newChild(mdWrap, "xmlData")
  fits = newChild(xmlData, "fits")
  fits.set("xmlns", "http://hul.harvard.edu/ois/xml/ns/fits/fits_output")
  fits.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
  fits.set("version", "0.3.2")
  fits.set("xsi:schemaLocation", "http://hul.harvard.edu/ois/xml/ns/fits/fits_output http://hul.harvard.edu/ois/xml/xsd/fits/fits_output.xsd")
  
  fitsTree = etree.parse(sys.argv[1]+"/FITS-"+ uuid + "-" + os.path.basename(filename)+".xml")
  fitsRoot = fitsTree.getroot()
  fits.append(fitsRoot)


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
      #myuuid = uuid.uuid4()
      myuuid=""
      pathSTR = string.replace(itempath.__str__(),"/tmp/" + sys.argv[2] + "/" + sys.argv[3], "objects", 1)
      if pathSTR in UUIDsDic:
        myuuid = UUIDsDic[pathSTR]
      else:
        print "Error - Log has no UUID for file: " + pathSTR + "{" + path.__str__() + "}"
      createDigiprovMD(myuuid, itempath)
      fileI = newChild(parentBranch, "file")
      fileI.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
      filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
      #filename = replace /tmp/"UUID" with /objects/

      
      fileI.set("ID", "file-" + myuuid.__str__())

      Flocat = newChild(fileI, "Flocat")
      Flocat.set("xlink:href", pathSTR + "/" + filename)
      Flocat.set("locType", "other")
      Flocat.set("otherLocType", "system")

      # structMap file
      div = newChild(structMapParent, "div")
      fptr = newChild(div, "fptr")
      fptr.set("FILEID","file-" + myuuid.__str__())

def tabify(root, last, indent):

  if last and last.text == "":
    i = 0
    last.text = "\n"
    while i < indent:
      last.text= last.text + "\t"
      i += 1
  if last:
    i = 0
    last.tail = "\n"
    while i < indent:
      last.tail= last.tail + "\t"
      i += 1    
  previous = root
  for element in root:
      previous = tabify(element,previous,indent+1)

  if previous and previous != root:
    i = 0
    previous.tail = "\n"
    while i < indent:
      previous.tail= previous.tail + "\t"
      i += 1
    if previous.text == "":
      i = 0
      previous.text = "\n\t"
      while i < indent:
        previous.text= previous.text + "\t"
        i += 1
  return root
      
if __name__ == '__main__':


  root = etree.Element("mets")
  root.text = "\n\t"
  root.set("xmlns:mets", "http://www.loc.gov/METS/")
  root.set("xmlns:premis", "info:lc/xmlns/premis-v2")
  root.set("xmlns:dcterms", "http://purl.org/dc/terms/")
  root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
#  root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
  root.set("xsi:schemaLocation", "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version18/mets.xsd info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd")

  #cd /tmp/$UUID; 
  opath = os.getcwd()
  os.chdir("/tmp/" + sys.argv[2])
  path = os.getcwd()

  loadDetoxDic()
  loadFileUUIDsDic()

  amdSec = newChild(root, "amdSec")

  fileSec = etree.Element("fileSec")
  fileSec.tail = "\n"
  root.append(fileSec)

  sipFileGrp = etree.Element("fileGrp")
  sipFileGrp.tail = "\n"
  sipFileGrp.set("ID", sys.argv[2].__str__())
  sipFileGrp.set("USE", "Objects package")
  fileSec.append(sipFileGrp)

  structMap = newChild(root, "structMap")
  structMapDiv = newChild(structMap, "div")
	
  createFileSec(path, sipFileGrp, structMapDiv)

  #tabify(root, root, 0)

  tree = etree.ElementTree(root)
  tree.write(sys.argv[1]+"/METS.xml")

  # Restore original path
  os.chdir(opath)
  
