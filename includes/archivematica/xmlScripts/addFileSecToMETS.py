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



def newChild(parent, tag, text=None, tailText=None):
  child = etree.Element(tag)
  parent.append(child)
  child.text = text
  if child.tail:
    child.tail = tailText
  else :
    child.tail = "\n"   
  return child




def createFileSec(path, parentBranch, indent):
  filename = os.path.basename(path)
  filename = string.replace(filename, sys.argv[2], "objects", 1)
  parentBranch.set("ID", filename)

  for item in os.listdir(path):
    itempath = os.path.join(path, item)
    if os.path.isdir(itempath):
      currentBranch = newChild(parentBranch, "fileGrp")
      currentBranch.set("USE", "directory")
      createFileSec(os.path.join(path, item), currentBranch, indent+1)    
    elif os.path.isfile(itempath):
      myuuid = uuid.uuid4()
      fileI = newChild(parentBranch, "file")
      filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
      #filename = replace /tmp/"UUID" with /objects/
      pathSTR = string.replace(path.__str__(),"/tmp/"+ sys.argv[2], "objects", 1)
      
      fileI.set("ID", "file-" + myuuid.__str__())

      Flocat = newChild(fileI, "Flocat")
      Flocat.set("xlink:href", pathSTR + "/" + filename)
      Flocat.set("locType", "other")
      Flocat.set("otherLocType", "system")
      
if __name__ == '__main__':
  #cd /tmp/$UUID; 
  opath = os.getcwd()
  os.chdir("/tmp/" + sys.argv[2])
  path = os.getcwd()

  if not os.path.isfile(sys.argv[1]+"/METS.xml"):
    print("System error")

  tree = etree.parse(sys.argv[1]+"/METS.xml")
  root = tree.getroot()


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
	
  createFileSec(path, sipFileGrp, 2)
  
  tree.write(sys.argv[1]+"/METS.xml")
	
  # Restore original path
  os.chdir(opath)
  
