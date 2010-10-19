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
import sys
import lxml.etree as etree

def newChild(parent, tag, text=None, tailText=None):
  child = etree.Element(tag)
  parent.append(child)
  child.text = text
  child.tail = tailText
  return child
      
def loadDublin(root, dublincore):      
#  dtree = etree.parse("/home/demo/ingestLogs/" + sys.argv[2] + "/DublinCore.xml")
#  droot = dtree.getroot()
#  child = newChild(root,  "dmdSec")
  child = etree.Element("dmdSec")
  root.insert(0, child)
  child.set("ID", "SIP-description")
  child = newChild(child, "mdWrap")
  child = newChild(child, "xmlData")
  child.append(dublincore)

if __name__ == '__main__':
  if not os.path.isfile(sys.argv[1]+"/METS.xml"):
    print("Archivematica error - METS.xml doesn't exist")

  tree = etree.parse(sys.argv[1]+"/METS.xml")
  root = tree.getroot()

  dtree = etree.parse(sys.argv[2]+"/dublincore.xml")
  dublincore = dtree.getroot()

  loadDublin(root, dublincore)
  
  tree.write(sys.argv[1]+"/METS.xml")

