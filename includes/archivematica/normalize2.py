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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.


# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#!/usr/bin/python
import os.path
import os
import sys
import logging
import subprocess
import shlex
import xml.etree.cElementTree as etree


#CONFIGURE THE FOLLOWING DIRECTORIES
accessFileDirectory = ""
fileDirectory = ""
logsDirectory = "/home/demo/ingestLogs/"
failedConversionsDirectory = "/home/demo/SIPerrors/normalizationErrors/"


#CONFIGURE THE FOLLOWING APPLICATION PATHS
#normalizationConfPath = "/mnt/userver910/archivematica2/includes/archivematica/normalizationConf"
normalizationConfPath = "/opt/archivematica/normalizationConf"
convertPath = "/usr/bin/convert " #Images
ffmpegPath = "/usr/bin/ffmpeg -i " #Audio
theoraPath = "/usr/bin/ffmpeg2theora "
unoconvPath = "/usr/bin/unoconv "
xenaPath = "java -jar /opt/externals/xena/xena.jar -f %fileFullName% -o %fileDirectory% -p /opt/externals/xena/plugins/" #Xena
#...Path = "" #Video
#...Path = "" #...

#SET THE DEFAULT COMMAND
defaultCommand = "java -jar /opt/externals/xena/xena.jar -f %fileFullName% -o %fileDirectory% -p /opt/externals/xena/plugins/"



#this script is passed fileIn, uuid
fileIn = sys.argv[1]
#fileUUID = sys.argv[2]

#get file name and extension
s = fileIn
#get indexes for python string array
#index of next char after last /
x1 = s.rfind('/')+1
#index of last .
x2 = s.rfind('.')
#index of next char after last .
x2mod = x2+1
#length of s
sLen = len(s)

fileTitle = s[x1:x2]
fileExtension = s[x2mod:sLen]
fileDirectory = s[:x1]
fileFullName = fileDirectory + fileTitle + "." + fileExtension

retval = False
try2 = False


def findDirectory(root, tag=None, text=None):
	ret = []
	if (not tag) and (not text):
		#return all
		for element in root:
			ret.append(element)
	else:
		if tag:
			if not text:
				#match the tag
				for element in root:
					if element.tag == tag:
						ret.append(element)
			else:
				#match tag and text
				for element in root:
					if element.tag == tag and element.text == text:
						ret.append(element)
		else:
			#match the text
			for element in root:
				if element.text == text:
					ret.append(element)
	return ret

	
def fillAttrib( attrib, var, fileExtension ):
  tree = etree.parse(normalizationConfPath + "/" + fileExtension.upper() + ".xml")
  root = tree.getroot()
#  print(etree.tostring(root))
 
  varsxml = findDirectory(root, "parent")
  if varsxml[0].text :
    return fillAttrib( attrib, var, varsxml[0].text )
  
  varsxml = findDirectory(root, attrib)
  for varxml in varsxml:
    var.append(varxml.text)
#  print var


parent = []
accessFormat = []
preservationFormat = []
accessConversionComand = []
preservationConversionComand =	[]


def executeCommand(command):

  #Replace replacement strings
  replacementDic = { \
  "%convertPath%": convertPath, \
  "%ffmpegPath%": ffmpegPath, \
  "%theoraPath%": theoraPath, \
  "%unoconvPath%": unoconvPath, \
  "%xenaPath%": xenaPath, \
  "%fileExtension%": fileExtension, \
  "%fileFullName%": fileFullName, \
  "%accessFileDirectory%": fileDirectory, \
  "%preservationFileDirectory%": fileDirectory, \
  "%fileDirectory%": fileDirectory,\
  "%fileTitle%": fileTitle, \
  "%accessFormat%": accessFormat[0], \
  "%preservationFormat%": preservationFormat[0] }
  
  
  #for each key replace all instances of the key in the command string
  for key in replacementDic.iterkeys():
    command = command.replace ( key, replacementDic[key] )

  #execute command
  try:
    if command != []:
      print >>sys.stderr, "processing: " + command.__str__()
      retcode = subprocess.call( shlex.split(command) )
      #it executes check for errors
      if retcode != 0:
        print >>sys.stderr, "error code:" + retcode.__str__()
      else:
        print >>sys.stderr, "executed OK"
        return 0
    else:
      print >>sys.stderr, "no conversion for type: " 
      return 1
	#catch OS errors
  except OSError, ose:
  	print >>sys.stderr, "Execution failed:", ose
  	return 1



try:
  fillAttrib("parent", parent, fileExtension)
  fillAttrib("accessFormat", accessFormat, fileExtension)
  fillAttrib("preservationFormat", preservationFormat, fileExtension)
  fillAttrib("accessConversionComand", accessConversionComand, fileExtension)
  fillAttrib("preservationConversionComand", preservationConversionComand, fileExtension)

except OSError, ose:
  print >>sys.stderr, "No normalization", ose
except IOError, ose:
  #NO config file for this extension
  
  #reset variables, to be sure
  parent = []
  accessFormat = []
  preservationFormat = []
  accessConversionComand = []
  preservationConversionComand =	[]
  
  #add default command (xena) to preservationConversionComand
  preservationConversionComand.append(defaultCommand)
  
#file not exist - no preservation format/malformed conf specified for .fileExtension



#if the file is not in access format
if len(accessConversionComand) > 0 :
    result = 1
    index = 0
    while(result and len(accessConversionComand) > index):
      if(len(accessFormat) > 0 and accessFormat[0].upper() == fileExtension.upper()):
        result = 0
        print "Already in access format. No need to normalize."
        continue
      accessFormat.append("")# just make it work :)
      preservationFormat.append("")
      result = executeCommand(accessConversionComand[index])
      index += 1
    if result:
      print "!!! ACCESS NORMALIZATION FAILED !!!"
else:
  print "No access normalization performed."

#if the file is not in preservation format
if len(preservationConversionComand) > 0:
    result = 1
    index = 0
    while(result and len(preservationConversionComand) > index):
      if(len(preservationFormat) > 0 and preservationFormat[0].upper() == fileExtension.upper()):
        result = 0
        print "Already in preservation format. No need to normalize."
        continue
      accessFormat.append("")
      preservationFormat.append("")
      result = executeCommand(preservationConversionComand[index])
      index += 1
    if result:
      print "!!! PRESERVATION NORMALIZATION FAILED !!!"
else:
  print "No preservation normalization performed."
#check to see if the file was created





