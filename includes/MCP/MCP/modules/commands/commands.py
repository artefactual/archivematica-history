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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

  #Replace replacement strings

import sys
import xml.etree.ElementTree as etree

class commandsClass():
    descriptionWhileExecuting = ""
    skip = True
    notification = ""
    execute = ""
    arguments = ""
    executeOnEachFile = True

    def getTagged(self, root, tag):
        ret = []
        for element in root:
            if element.tag == tag:
                ret.append(element)
        if len(ret) != 1 :
            print "error in config file"
        return ret    

    def __init__(self, xml):
        self.descriptionWhileExecuting = self.getTagged(xml, "descriptionWhileExecuting")[0].text
        self.identifier = self.getTagged(xml, "identifier")[0].text
        self.standardIn = self.getTagged(xml, "standardIn")[0].text
        self.standardOut = self.getTagged(xml, "standardOut")[0].text
        self.standardError = self.getTagged(xml, "standardError")[0].text
        self.skip = self.getTagged(xml, "skip")[0].text.lower() != "no"
        self.failureNotification = self.getTagged(xml, "failureNotification")[0].text
        self.execute = self.getTagged(xml, "execute")[0].text
        self.arguments = self.getTagged(xml, "arguments")[0].text
        self.executeOnEachFile = self.getTagged(xml, "executeOnEachFile")[0].text.lower() != "no"
        self.filterFileStart = self.getTagged(xml, "filterFileStart")[0].text
        self.filterFileEnd = self.getTagged(xml, "filterFileEnd")[0].text
        
    def __str__(self):
        ret = self.descriptionWhileExecuting
        return ret







"""
  replacementDic = { \
  "%convertPath%": convertPath, \
  "%ffmpegPath%": ffmpegPath, \
  "%theoraPath%": theoraPath, \
  "%unoconvPath%": unoconvPath, \
  "%xenaPath%": xenaPath, \
  "%fileExtension%": fileExtension, \
  "%fileFullName%": fileFullName, \
  "%accessFileDirectory%": accesspath, \
  "%preservationFileDirectory%": fileDirectory, \
  "%fileDirectory%": fileDirectory,\
  "%fileTitle%": fileTitle, \
  "%normalizationScriptsDir%": normalizationScriptsDir, \
  "%accessFormat%": accessFormat[0].lower(), \
  "%preservationFormat%": preservationFormat[0].lower() }
  
  #for each key replace all instances of the key in the command string
  for key in replacementDic.iterkeys():
    command = command.replace ( key, replacementDic[key] )
    
"""
