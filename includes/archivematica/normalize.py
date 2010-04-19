#!/usr/bin/python

import os.path
import os
import sys
import logging

#this script is passed fileIn, fileType, uuid
fileIn = sys.argv[1]
#fileType = sys.argv[2]
if sys.argv[2]:
    fileUUID = sys.argv[2]
else:
    fileUUID = "9999"

#CONFIGURE THE FOLLOWING DIRECTORIES
accessFileDirectory = ""
archiveFileDirectory = ""
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
fileName = archiveFileDirectory + fileTitle + "." + fileExtension

retval = False
try2 = False

#CONFIGURE THE FOLLOWING APPLICATION PATHS
convertPath = "/usr/bin/convert " #Images
ffmpegPath = "/usr/bin/ffmpeg -i " #Audio
theoraPath = "/usr/bin/ffmpeg2theora "
unoconvPath = "/usr/bin/unoconv "
#...Path = "" #Video
#...Path = "" #...
xenaPath = "" #Xena

conversionDict = {}

#********************************************
#Audio - AC3, MP3, WAV, WMA
#********************************************

conversionDict['AC3'] = {}
conversionDict['AC3']['archiveFormat'] = "WAV"
conversionDict['AC3']['accessFormat'] = "MP3"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['AC3']['PrimaryAccessConversionComand'] = ffmpegPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['AC3']['accessFormat'].lower()
conversionDict['AC3']['PrimaryArchiveConversionComand'] = ffmpegPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['AC3']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['AC3']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['AC3']['archiveFormat'].lower()
conversionDict['AC3']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['AC3']['archiveFormat'].lower()

conversionDict['MP3'] = {}
conversionDict['MP3']['archiveFormat'] = "WAV"
conversionDict['MP3']['accessFormat'] = "MP3"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['MP3']['PrimaryAccessConversionComand'] = ffmpegPath + fileName + " " + accessFileDirectory  + fileTitle + "." + conversionDict['MP3']['accessFormat'].lower()
conversionDict['MP3']['PrimaryArchiveConversionComand'] = ffmpegPath + fileName + " " + archiveFileDirectory  + fileTitle + "." + conversionDict['MP3']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['MP3']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['MP3']['accessFormat'].lower()
conversionDict['MP3']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['MP3']['archiveFormat'].lower()

conversionDict['WAV'] = {}
conversionDict['WAV']['archiveFormat'] = "WAV"
conversionDict['WAV']['accessFormat'] = "MP3"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['WAV']['PrimaryAccessConversionComand'] = ffmpegPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['WAV']['accessFormat'].lower()
conversionDict['WAV']['PrimaryArchiveConversionComand'] = ffmpegPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['WAV']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['WAV']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['WAV']['accessFormat'].lower()
conversionDict['WAV']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['WAV']['archiveFormat'].lower()

conversionDict['WMA'] = {}
conversionDict['WMA']['archiveFormat'] = "WAV"
conversionDict['WMA']['accessFormat'] = "MP3"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['WMA']['PrimaryAccessConversionComand'] = ffmpegPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['WMA']['accessFormat'].lower()
conversionDict['WMA']['PrimaryArchiveConversionComand'] = ffmpegPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['WMA']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['WMA']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['WMA']['accessFormat'].lower()
conversionDict['WMA']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['WMA']['archiveFormat'].lower()

#********************************************
#Presentation files - PPT
#********************************************

conversionDict['PPT'] = {}
conversionDict['PPT']['archiveFormat'] = "PDF"
conversionDict['PPT']['accessFormat'] = "ODP"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['PPT']['PrimaryAccessConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['PPT']['accessFormat'].lower() + " " +fileName
conversionDict['PPT']['PrimaryArchiveConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['PPT']['archiveFormat'].lower() + " " +fileName 
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['PPT']['AltAccessConversionComand'] = xenaPath
conversionDict['PPT']['AltArchiveConversionComand'] = xenaPath 

#********************************************
#Images - BMP, GIF, JPG, JP2, PNG, TIFF, TGA
#********************************************

conversionDict['BMP'] = {}
conversionDict['BMP']['archiveFormat'] = "TIF"
conversionDict['BMP']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['BMP']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['BMP']['accessFormat'].lower()
conversionDict['BMP']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['BMP']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['BMP']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['BMP']['accessFormat'].lower()
conversionDict['BMP']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['BMP']['archiveFormat'].lower()

conversionDict['GIF'] = {}
conversionDict['GIF']['archiveFormat'] = "TIF"
conversionDict['GIF']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['GIF']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['GIF']['accessFormat'].lower()
conversionDict['GIF']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['GIF']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['GIF']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['GIF']['accessFormat'].lower()
conversionDict['GIF']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['GIF']['archiveFormat'].lower()

conversionDict['JPG'] = {}
conversionDict['JPG']['archiveFormat'] = "TIF"
conversionDict['JPG']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['JPG']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['JPG']['accessFormat'].lower()
conversionDict['JPG']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['JPG']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['JPG']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['JPG']['accessFormat'].lower()
conversionDict['JPG']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['JPG']['archiveFormat'].lower()

conversionDict['JP2'] = {}
conversionDict['JP2']['archiveFormat'] = "TIF"
conversionDict['JP2']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['JP2']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['JP2']['accessFormat'].lower()
conversionDict['JP2']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['JP2']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['JP2']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['JP2']['accessFormat'].lower()
conversionDict['JP2']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['JP2']['archiveFormat'].lower()

conversionDict['PNG'] = {}
conversionDict['PNG']['archiveFormat'] = "TIF"
conversionDict['PNG']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['PNG']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['PNG']['accessFormat'].lower()
conversionDict['PNG']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['PNG']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['PNG']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['PNG']['accessFormat'].lower()
conversionDict['PNG']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['PNG']['archiveFormat'].lower()

conversionDict['TIFF'] = {}
conversionDict['TIFF']['archiveFormat'] = "TIF"
conversionDict['TIFF']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['TIFF']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['TIFF']['accessFormat'].lower()
conversionDict['TIFF']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['TIFF']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['TIFF']['AltAccessConversionComand'] = xenaPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['TIFF']['accessFormat'].lower()
conversionDict['TIFF']['AltArchiveConversionComand'] = xenaPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['TIFF']['archiveFormat'].lower()

conversionDict['TGA'] = {}
conversionDict['TGA']['archiveFormat'] = "TIF"
conversionDict['TGA']['accessFormat'] = "JPG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['TGA']['PrimaryAccessConversionComand'] = convertPath + fileName + " +compress " + accessFileDirectory  + fileTitle + "." + conversionDict['TGA']['accessFormat'].lower()
conversionDict['TGA']['PrimaryArchiveConversionComand'] = convertPath + fileName + " +compress " + archiveFileDirectory  + fileTitle + "." + conversionDict['TGA']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['TGA']['AltAccessConversionComand'] = xenaPath
conversionDict['TGA']['AltArchiveConversionComand'] = xenaPath

#********************************************
#Raw camera files - NEF
#********************************************

conversionDict['NEF'] = {}
conversionDict['NEF']['archiveFormat'] = "DNG"
conversionDict['NEF']['accessFormat'] = "JPEG"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['NEF']['PrimaryAccessConversionComand']=""
conversionDict['NEF']['PrimaryArchiveConversionComand']=""
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['NEF']['AltAccessConversionComand']=""
conversionDict['NEF']['AltArchiveConversionComand']=""

#********************************************
#Spreadsheets - XLS
#********************************************

conversionDict['XLS'] = {}
conversionDict['XLS']['archiveFormat'] = "ODS"
conversionDict['XLS']['accessFormat'] = "XLS"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['XLS']['PrimaryAccessConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['XLS']['accessFormat'].lower() + " " +fileName 
conversionDict['XLS']['PrimaryArchiveConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['XLS']['archiveFormat'].lower() + " " +fileName  
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['XLS']['AltAccessConversionComand'] = xenaPath
conversionDict['XLS']['AltArchiveConversionComand'] = xenaPath 


#********************************************
#Video - AVI, FLV, MOV, MPEG, SWF, WMV
#********************************************

conversionDict['WMV'] = {}
conversionDict['WMV']['archiveFormat'] = "MXF"
conversionDict['WMV']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['WMV']['PrimaryAccessConversionComand']=  theoraPath + fileName
conversionDict['WMV']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['WMV']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['WMV']['AltAccessConversionComand']=""
conversionDict['WMV']['AltArchiveConversionComand']=""

conversionDict['MPG'] = {}
conversionDict['MPG']['archiveFormat'] = "MXF"
conversionDict['MPG']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['MPG']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['MPG']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['MPG']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['MPG']['AltAccessConversionComand']=""
conversionDict['MPG']['AltArchiveConversionComand']=""

conversionDict['SWF'] = {}
conversionDict['SWF']['archiveFormat'] = "MXF"
conversionDict['SWF']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['SWF']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['SWF']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['SWF']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['SWF']['AltAccessConversionComand']=""
conversionDict['SWF']['AltArchiveConversionComand']=""

conversionDict['FLV'] = {}
conversionDict['FLV']['archiveFormat'] = "MXF"
conversionDict['FLV']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['FLV']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['FLV']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['FLV']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['FLV']['AltAccessConversionComand']=""
conversionDict['FLV']['AltArchiveConversionComand']=""

conversionDict['MOV'] = {}
conversionDict['MOV']['archiveFormat'] = "MXF"
conversionDict['MOV']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['MOV']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['MOV']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['MOV']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['MOV']['AltAccessConversionComand']=""
conversionDict['MOV']['AltArchiveConversionComand']=""

conversionDict['AVI'] = {}
conversionDict['AVI']['archiveFormat'] = "MXF"
conversionDict['AVI']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['AVI']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['AVI']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['AVI']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['AVI']['AltAccessConversionComand']=""
conversionDict['AVI']['AltArchiveConversionComand']=""

conversionDict['MP4'] = {}
conversionDict['MP4']['archiveFormat'] = "MXF"
conversionDict['MP4']['accessFormat'] = "OGV"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['MP4']['PrimaryAccessConversionComand']= theoraPath + fileName
conversionDict['MP4']['PrimaryArchiveConversionComand']= ffmpegPath + fileName + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 4800 " + accessFileDirectory  + fileTitle + "." + conversionDict['MP4']['archiveFormat'].lower()
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['MP4']['AltAccessConversionComand']=""
conversionDict['MP4']['AltArchiveConversionComand']=""

#********************************************
#Word processing files - DOC,WPD
#********************************************

conversionDict['DOC'] = {}
conversionDict['DOC']['archiveFormat'] = "ODT"
conversionDict['DOC']['accessFormat'] = "PDF"
#using primary tool - CONFIGURE COMMAND BELOW
conversionDict['DOC']['PrimaryAccessConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['DOC']['accessFormat'].lower() + " " +fileName 
conversionDict['DOC']['PrimaryArchiveConversionComand'] = unoconvPath + " -v --server localhost -f " + conversionDict['DOC']['archiveFormat'].lower() + " " +fileName  
#using secondary tool, usually xena - CONFIGURE COMMAND BELOW
conversionDict['DOC']['AltAccessConversionComand'] = xenaPath
conversionDict['DOC']['AltArchiveConversionComand'] = xenaPath 



#create log file Directory if needed
def check_path():
    if os.path.exists(logsDirectory + fileUUID):
        return True
    else:
        os.mkdir( logsDirectory + fileUUID )

check_path()
#setup logging
LOG_FILENAME = '/home/demo/ingestLogs/'+fileUUID+'/normalization.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def check_files():
#does extension have a key in Dictionary? can we convert it?
  if conversionDict.has_key(fileExtension.upper()):
    return True
  else:
    return False
#get Command from Dictionary for appropriate pass at conversion (this allows for finest granularity)
#each fileType has four Commands that must be individually configured in Dictionary above
def get_command(type, pass_type ):
#only four possible Commands per fileType
        if (type == "access"):
            if (pass_type == "primary"):
                command = conversionDict[fileExtension.upper()]['PrimaryAccessConversionComand']
            else:
                command = conversionDict[fileExtension.upper()]['AltAccessConversionComand']
        else:
            if (pass_type == "primary"):
                command = conversionDict[fileExtension.upper()]['PrimaryArchiveConversionComand']
            else:
                command = conversionDict[fileExtension.upper()]['AltArchiveConversionComand']
        return command;

#based on Type return full Path and Name used in order to check if file has been created
def get_file_in_path(type):
      if (type == "access"):
          fileInPath=accessFileDirectory+fileTitle+"."+conversionDict[fileExtension.upper()]['accessFormat'].lower()
      if (type == "archive"):
          fileInPath=archiveFileDirectory+fileTitle+"."+conversionDict[fileExtension.upper()]['archiveFormat'].lower()
      return fileInPath

#all files converted using only one function
def convert_files(type, pass_type ): #pass Type = Primary or Alternate?
  if check_files():
      try:
        command = get_command(type, pass_type )
        os.system(command)
#catch both OS errors and standard errors
      except OSError, ose:
        logging.exception("Access "+type+" Type file conversion failed - OS error for "+type+" "+fileIn )
#check for converted file... if file doesnt exist it wasnt converted, call again using Alternate Command
      fileInPath = get_file_in_path(type)
#cold hard check - did we produce file?
      if os.path.isfile(fileInPath):
          return True
#if not try secondary tool
      else:
          if pass_type == "primary":
             convert_files( type , "alt")
#did Alternate tool produce file?
             if os.path.isfile(fileInPath):
                return True
             else:
#else log failure and copy file
                mvCmd = "cp "+fileIn +" "+failedConversionsDirectory
                logging.debug(mvCmd)
                os.system( mvCmd )
                logging.debug("Failed both attempts at converting "+type+" Type file "+fileIn+". Copied file to Failed "+type+" Conversions Directory" )
                return False

convert_files("access", "primary")
convert_files("archive", "primary")
