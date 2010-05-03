#!/usr/bin/python

import os.path
import os
import sys
import logging
import subprocess
import shlex
import xml.etree.cElementTree as etree


#this script is passed fileIn, uuid
fileIn = sys.argv[1]
#fileType = sys.argv[2]
if sys.argv[2]:
    fileUUID = sys.argv[2]
else:
    fileUUID = "9999"

#CONFIGURE THE FOLLOWING DIRECTORIES
accessFileDirectory = ""
fileDirectory = ""
logsDirectory = "/home/demo/ingestLogs/"
failedConversionsDirectory = "/home/demo/SIPerrors/normalizationErrors/"

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
fileName = fileDirectory + fileTitle + "." + fileExtension

retval = False
try2 = False

#CONFIGURE THE FOLLOWING APPLICATION PATHS
#normalizationConfPath = "/mnt/userver910/archivematica2/includes/archivematica/normalizationConf"
normalizationConfPath = "/opt/includes/archivematica/normalizationConf"
convertPath = "/usr/bin/convert " #Images
ffmpegPath = "/usr/bin/ffmpeg -i " #Audio
theoraPath = "/usr/bin/ffmpeg2theora "
unoconvPath = "/usr/bin/unoconv "
xenaPath = "java -jar /opt/externals/xena/xena.jar -f $1 -o $2 -p plugins/" #Xena
#...Path = "" #Video
#...Path = "" #...




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
  print var


parent = []
accessFormat = []
archiveFormat = []
accessConversionComand = []
archiveConversionComand =	[]






def executeCommand(command):

  #Replace replacement strings
  replacementDic = { \
  "%convertPath%": convertPath, \
  "%ffmpegPath%": ffmpegPath, \
  "%theoraPath%": theoraPath, \
  "%unoconvPath%": unoconvPath, \
  "%xenaPath%": xenaPath, \
  "%fileExtension%": fileExtension, \
  "%fileName%": fileName, \
  "%accessFileDirectory%": fileDirectory, \
  "%archiveFileDirectory%": fileDirectory, \
  "%fileTitle%": fileTitle, \
  "%accessFormat%": accessFormat[0], \
  "%archiveFormat%": archiveFormat[0] }
  
  
  #for each key replace all instances of the key in the command string
  for key in replacementDic.iterkeys():
    command = command.replace ( key, replacementDic[key] )

  #execute command
  try:
    if command != []:
      print >>sys.stderr, "processing: " + shlex.split(command).__str__()
      retcode = subprocess.call( shlex.split(command) )
      #it executes check for errors
      if retcode != 0:
        print >>sys.stderr, "error code:" + retcode.__str__()
      else:
        print >>sys.stderr, "executed OK"
    else:
      print >>sys.stderr, "no conversion for type: " 
	#catch OS errors
  except OSError, ose:
  	print >>sys.stderr, "Execution failed:", ose






try:
  fillAttrib("parent", parent, fileExtension)
  fillAttrib("accessFormat", accessFormat, fileExtension)
  fillAttrib("archiveFormat", archiveFormat, fileExtension)
  fillAttrib("accessConversionComand", accessConversionComand, fileExtension)
  fillAttrib("archiveConversionComand", archiveConversionComand, fileExtension)

except OSError, ose:
      	print >>sys.stderr, "No normalization", ose
#file not exist - no archive format/malformed conf specified for .fileExtension


#if the file is not in access format
if accessFormat[0].upper() != fileExtension.upper():
  result = 1
  index = 0
  while(result and accessConversionComand[index] ):
   result = executeCommand(accessConversionComand[index])
  if result:
    error

#if the file is not in archive format
if archiveFormat[0].upper() != fileExtension.upper():
  result = 1
  index = 0
  while(result and archiveConversionComand[index] ):
   result = executeCommand(archiveConversionComand[index])
  if result:
    error

#check to see if the file was created





