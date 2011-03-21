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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import lxml.etree as etree

def getTagged(root, tag):
    ret = []
    for element in root:
        #print element.tag 
        #print tag
        #print element.tag == tag
        if element.tag == tag:
            ret.append(element)
            #return ret #only return the first encounter
    return ret  

def getPronomsFromPremis(filePath):
    tree = etree.parse( filePath )
    root = tree.getroot()
    ret = []
    objects = getTagged(root, "object")
    if len(objects):
        objectCharacteristics = getTagged(objects[0], "objectCharacteristics")
        if len(objectCharacteristics):
            formats = getTagged(objectCharacteristics[0], "format")
            for format in formats:
                formatRegistrys = getTagged(format, "formatRegistry")
                for formatRegistry in formatRegistrys:
                    if getTagged(formatRegistry, "formatRegistryName")[0].text == "PRONOM":
                        ret.append(getTagged(formatRegistry, "formatRegistryKey")[0].text)
    return ret  