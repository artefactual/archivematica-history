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
# @version svn: $Id$


import os
import uuid
import sys
import xml.etree.cElementTree as etree
from xml.sax.saxutils import quoteattr as xml_quoteattr


def newChild( parent, tag, text=None, tailText=None ):
	child = etree.Element(tag)
	parent.append(child)
	child.text = text
	child.tail = tailText
	return child

def DirAsLessXML( path, parentBranch ):
	currentBranch = newChild(parentBranch,"dir")
	filename = os.path.basename(path)
	currentBranch.set("name", filename)
	currentBranch.set("originalName", filename)
	
	for item in os.listdir(path):
		itempath = os.path.join(path, item)
		if os.path.isdir(itempath):
				DirAsLessXML(os.path.join(path, item), currentBranch)
		elif os.path.isfile(itempath):
			myuuid = uuid.uuid4()
			fileI = newChild(currentBranch, "file")
			filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
			newChild(fileI, "name", filename, None )
			newChild(fileI, "originalName", filename, None )
			newChild(fileI, "UUID", myuuid.__str__())

  
if __name__ == '__main__':
	#cd /tmp/$UUID; 
	opath = os.getcwd()
	os.chdir("/tmp/" + sys.argv[2])
	path = os.getcwd()

	if not os.path.isfile(sys.argv[1]+"/SIP.xml"):
		print("SIPdoesn't exist... creating.")
#		/opt/archivematica/SIPxmlModifiers/CreateSipAndAddDublinCoreStructure.py

	tree = etree.parse(sys.argv[1]+"/SIP.xml")
	root = tree.getroot()
	
	DirAsLessXML(path,root)
	
	tree.write(sys.argv[1]+"/SIP.xml")
	
	#restore original path
	os.chdir(opath)

