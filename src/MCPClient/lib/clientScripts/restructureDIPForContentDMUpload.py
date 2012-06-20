#!/usr/bin/python -OO


# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
# @author Mark Jordan <email>
# @version svn: $Id$

import argparse
import os
import sys
import glob
import shutil
import json
import urllib
import csv
import collections
import zipfile
import pprint # remove for production
from xml.dom.minidom import parse, parseString

# Create the output dir for the CONTENTdm DIP. importMethod is either 'projectclient'
# or 'directimport'. Also return the path. 
def prepareOutputDir(outputDipDir, importMethod, dipUuid):
    outputDipDir = os.path.join(outputDipDir, importMethod, dipUuid)
    # Check for and then delete a subdirectory named after the current package. We always want
    # a clean output directory for the import package.
    if os.path.exists(outputDipDir):
        shutil.rmtree(outputDipDir)
    os.makedirs(outputDipDir)
    return outputDipDir


# Takes in a DOM object containing the Dublin Core XML, returns a dictionary with 
# tag : [ value1, value2] members. Also, since minidom only handles byte strings
# so we need to encode strings before passing them to minidom functions.
def parseDcXml(dublincore):
    # Check to see if there is a title (required by CONTENTdm). If not, assign a 
    # placeholder title.
    dcTitlesDom = dublincore.getElementsByTagName('title')  # This is the line thowing the error
    if not dcTitlesDom:
        return {'title' : ['Placeholder title']} 

    # Get the element (regardless of namespace) found in the incoming DC XML DOM object.
    dcElementsDom = dublincore.getElementsByTagNameNS('*', '*')  # This is the line thowing the error
    dcElementsDict = {}
    for dcElement in dcElementsDom:
        # We only want elements that are not empty.
        if dcElement.firstChild: 
            # To get the values of repeated DC elements, we need to create a list to correspond to each
            # element name. If the element name is not yet a key in dcElementsDict, create the element's 
            # value list.
            if dcElement.tagName not in dcElementsDict:
                dcElementsDict[dcElement.tagName.encode( "utf-8" )] = [dcElement.firstChild.nodeValue.encode( "utf-8" )]
            # If the element name is present in dcElementsDict, append the element's value to its value list.
            else:
                dcElementsDict[dcElement.tagName.encode( "utf-8" )].append(dcElement.firstChild.nodeValue.encode( "utf-8" ))
    return dcElementsDict

# Takes in a DOM object containing the METS structMap, returns a dictionary with 
# fptrValue : [ order, parent, dmdSec, label, filename ] members.
# Files in the DIP objects directory start with the UUID (i.e., first 36 characters of the filename)
# of the of the file named in the fptr FILEID in the structMap; each file ends in the UUID.
# Also, we are only interested in divs that are direct children of a div with TYPE=directory and LABEL=objects:
#  <div TYPE="directory" LABEL="DigitizationOutput-50a3c71f-92d6-46d1-98ce-8227caa79f85-50a3c71f-92d6-46d1-98ce-8227caa79f85">
#      <div TYPE="directory" LABEL="objects" DMDID="dmdSec_1">
#        <div LABEL="Page 1">
#          <fptr FILEID="P1050152.JPG-e2d0cd78-f1b9-446b-81ae-ea0e282332bb"/>
#        </div>
def parseStructMap(structMap, filesInObjectDirectory):
    structMapDict = {}
    pp = pprint.PrettyPrinter(indent=4) # Remove after development.
    # Get filenames of all the files in the objects directory (recursively); filesInObjectDirectory contains
    # paths, we need to get the filename only for the structMap checking. Add each filename to structMapDict.
    filesInObjectDir = []
    for file in filesInObjectDirectory:
        head, tail = os.path.split(file)
        filesInObjectDir.append(tail)
        
    # Get all the fptr elements.
    fptrs = structMap.getElementsByTagName('fptr')
    fptrOrder = 0
    for node in structMap.getElementsByTagName('fptr'):
        for k, v in node.attributes.items():
            if k == 'FILEID':
                parentDivLabel = node.parentNode.getAttribute('LABEL')
                # Placeholder for when we support compound items with their own descriptive metadata.
                parentDivDmdId = node.parentNode.getAttribute('DMDID')
                # Assumes that divs containing fptrs have LABEL attributes.
                if len(parentDivLabel):
                    fptrOrder = fptrOrder + 1
                    # For each fptr, check to see if there is a matching file.
                    # @todo: Check to see if file exists? Or can we assume it does?
                    filename = getFptrObjectFilename(v, filesInObjectDir)
                    structMapDict[v] = {
                        # Python has no natsort, so we padd fptOrder with zeros to make it more
                        # easily sortable.
                        'order' : str(fptrOrder).zfill(5),
                        'parent' : '', # Placeholder for when we support hierarchical items.
                        'filename' : filename,
                        'label' : parentDivLabel,
                        'dmdSec' : parentDivDmdId
                    }
        

    return structMapDict

# Given a ftpr value (which looks like this: P1050154.JPG-09869659-fc89-46ce-ad1c-fe166becccca), return the
# name of the corresponding file from the DIP objects directory.
def getFptrObjectFilename(fptrValue, filesInObjectDir):
    # Assumes UUID is the last 36 characters of the fptr value.
    uuid = fptrValue[-36:]
    for filename in filesInObjectDir:
        if uuid in filename:
            return filename

# Generate a directory containing 1) 'mappings', a nested dictionary with DCTERMS elememts as keys,
# each of which has as its values the CONTENTdm nick and name for the corresponding field in the
# current collection and 2), 'order', a list of the collection's field nicks, which is needed
# to write out the metadata in the correct field order. Archivematica only uses the legacy
# unqualified DC elements but we include the entire CONTENTdm DCTERMS mappings for good measure.
def getContentdmCollectionFieldInfo(contentdmServer, targetCollection):
    collectionFieldInfo = {}
    pp = pprint.PrettyPrinter(indent=4) # Remove after development.
    # First, define the CONTENTdm DC nicknames -> DCTERMs mapping. 
    contentdmDctermsMap = {
         'describ' : 'abstract',
         'rightsa' : 'accessRights',
         'accrua' : 'accrualMethod',
         'accrub' : 'accrualPeriodicity',
         'accruc' : 'accrualPolicy',
         'titlea' : 'alternative',
         'audien' : 'audience',
         'datec' : 'available',
         'identia' : 'bibliographicCitation',
         'relatim' : 'conformsTo',
         'contri' : 'contributor',
         'covera' : 'coverage',
         'datea' : 'created',
         'creato' : 'creator',
         'date' : 'date',
         'datef' : 'dateAccepted',
         'dateg' : 'dateCopyrighted',
         'dateh' : 'dateSubmitted',
         'descri' : 'description',
         'audienb' : 'educationLevel',
         'formata' : 'extent',
         'format' : 'format',
         'relatil' : 'hasFormat',
         'relatih' : 'hasPart',
         'relatib' : 'hasVersion',
         'identi' : 'identifier',
         'instru' : 'instructionalMethod',
         'relatik' : 'isFormatOf',
         'relatig' : 'isPartOf',
         'relatii' : 'isReferencedBy',
         'relatic' : 'isReplacedBy',
         'relatie' : 'isRequiredBy',
         'relatia' : 'isVersionOf',
         'dated' : 'issued',
         'langua' : 'language',
         'rightsb' : 'license',
         'audiena' : 'mediator',
         'formatb' : 'medium',
         'datee' : 'modified',
         'proven' : 'provenance',
         'publis' : 'publisher',
         'relatij' : 'references',
         'relati' : 'relation',
         'relatid' : 'replaces',
         'relatif' : 'requires',
         'rights' : 'rights',
         'rightsc' : 'rightsHolder',
         'source' : 'source',
         'coveraa' : 'spatial',
         'subjec' : 'subject',
         'descria' : 'tableOfContents',
         'coverab' : 'temporal',
         'title' : 'title',
         'type' : 'type',
         'dateb' : 'valid',
    }
    # Query CONTENTdm to get the target collection's field configurations.
    CollectionFieldConfigUrl = 'http://' + contentdmServer + '/dmwebservices/index.php?q=dmGetCollectionFieldInfo' + targetCollection + '/json'
    f = urllib.urlopen(CollectionFieldConfigUrl)
    collectionFieldConfigString = f.read()
    collectionFieldConfig = json.loads(collectionFieldConfigString)
    # We want a dict containing items that looks like { 'contributor': { 'name': u'Contributors', 'nick': u'contri'},
    # 'creator': { 'name': u'Creator', 'nick': u'creato'}, 'date': { 'name': u'Date', 'nick': u'dateso'}, [...] }
    # We need these field-specific mappings when writing out metadata files for loading into CONTENTdm.
    # It is possible that more than one CONTENTdm field is mapped to the same DC element; in this case,
    # just take the last mapping and ignore the rest, since there is no way to tell which should take precedence.
    collectionFieldMappings = {}
    # We also want a simple list of all the fields in the current collection.
    collectionFieldOrder = [] 
    for fieldConfig in collectionFieldConfig:
        for k, v in fieldConfig.iteritems():
            if fieldConfig['dc'] != 'BLANK' and fieldConfig['dc'] != '':
               collectionFieldMappings[contentdmDctermsMap[fieldConfig['dc']]] = {'nick' : fieldConfig['nick'] , 'name' : fieldConfig['name']}
        collectionFieldOrder.append(fieldConfig['nick'])
    collectionFieldInfo['mappings'] = collectionFieldMappings
    collectionFieldInfo['order'] = collectionFieldOrder
    return collectionFieldInfo

# Return the dmdSec with the specific ID value. If dublinCore is True, return
# the <dublincore> child node only.
def getDmdSec(metsDom, dmdSecId = 'dmdSec_1', dublinCore = True):
    for node in metsDom.getElementsByTagName('dmdSec'):
        for k, v in node.attributes.items():
            if dublinCore and k == 'ID' and v == dmdSecId:
                # Assumes there is only one dublincore child element.
                return node.getElementsByTagName('dublincore')[0]
            else:
                return node

# Get a list of all the files (recursive) in the DIP object directory. Even though there
# can be subdirectories in the objects directory, assumes each file should have a unique name.
# Optionally include the paths for each file.
def getObjectDirectoryFiles(objectDir):
    fileList = []
    for root, subFolders, files in os.walk(objectDir):
        for file in files:
            fileList.append(os.path.join(root, file))
            # print "Debug: file is " + os.path.join(root, file)
    return fileList


# Create a .zip from the DIP file produced by generateXXProjectClientPackage functions.
# Zip files are written in the uploadedDIPs directory.
def zipProjectClientOutput(outputDipDir, dipUuid):
    outputFile = zipfile.ZipFile(outputDipDir + ".zip", "w")
    for sourceFilename in glob.glob(os.path.join(outputDipDir, '*')):
        # Prepend the UUID to the filename so the zip file will unzip into the corresponding
        # directory.
        destFilename = os.path.join(dipUuid, os.path.basename(sourceFilename))
        outputFile.write(sourceFilename, destFilename, zipfile.ZIP_DEFLATED)
    outputFile.close()

# Generate a .desc file used in CONTENTdm 'direct import' packages.
 # .desc file looks like this:
 # <?xml version="1.0" encoding="utf-8"?>
 # <itemmetadata>
 # <title>wall</title>
 #  [... every collection field, empty and with values]
 # <is></is>
 # <transc></transc>
 # <fullrs />
 # <dmoclcno></dmoclcno>
 # <dmcreated></dmcreated>
 # <dmmodified></dmmodified>
 # <dmrecord></dmrecord>
 # <find></find>
 # <dmimage></dmimage>
 # <dmad1></dmad1>
 # <dmad2></dmad2>
 # <dmaccess></dmaccess>
 # </itemmetadata>
# @todo: DC element names need to be converted to CONTENTdm nicknames.
def generateDescFile(dcMetadata):
    collectionFieldInfo = getContentdmCollectionFieldInfo(args.contentdmServer, args.targetCollection)
    output = '<?xml version="1.0" encoding="utf-8"?>' + "\n"
    output += "<itemmetadata>\n"
    for key in dcMetadata:
        # @todo: This dict value needs to be tested.
        output += '<' + collectionFieldInfo[key][nick] + '>'
        values = ''
        for v in dcMetadata[key]:
            values += v + '; '
        output += values.rstrip('; ')
        output += '</' + key + ">\n"
    output += "<is></is>\n"
    output += "<transc></transc>\n"
    output += "<fullrs />\n"
    output += "<dmoclcno></dmoclcno>\n"
    output += "<dmcreated></dmcreated>\n"
    output += "<dmmodified></dmmodified>\n"
    output += "<dmrecord></dmrecord>\n"
    output += "<find></find>\n"
    output += "<dmimage></dmimage>\n"
    output += "<dmad1></dmad1>\n"
    output += "<dmad2></dmad2>\n"
    output += "<dmaccess></dmaccess>\n"
    output += "</itemmetadata>\n"
    return output


# Generate a 'direct upload' (i.e., single object file) package for a simple item from the 
# Archivematica DIP. This package will contain the object file, its thumbnail, a .desc (DC metadata)
# file, and a .full (manifest) file.
def generateSimpleContentDMDirectUploadPackage(metsDom, dipUuid, outputDipDir, filesInObjectDirectory, filesInThumbnailDirectory):
    dmdSec = getDmdSec(metsDom)
    dcMetadata = parseDcXml(dmdSec)

    descFile = generateDescFile(dcMetadata)

    outputDipDir = prepareOutputDir(outputDipDir, 'directupload', dipUuid)

    print "Debug: files in thumbnail directory - " + filesInThumbnailDirectory
    print "Debug: outputDipDir - " + outputDipDir

    # In 0.9 dev, there is a thumbnails directory (sibling of objects and METS file) that
    # contains .jpg files with names the same as the front-end UUIDs (i.e., first 36 characters
    # of the object filename) of the files in the objects directory.

    # .full file looks like this:
 # <item>
 #  <title>wall</title>
 #  <object>142_58_131_27_2012-3-28_8525511-14722693060.jpg</object>
 #  <desc>142_58_131_27_2012-3-28_8525511-14722693060.desc</desc>
 #  <icon>142_58_131_27_2012-3-28_8525511-14722693060.icon</icon>
 #  <update>0</update>
 # <info>nopdf</info>
 # </item>


# Generate a 'project client' package for a simple item from the Archivematica DIP.
# This package will contain the object file and a delimited metadata file in a format
# suitable for importing into CONTENTdm using its Project Client.
def generateSimpleContentDMProjectClientPackage(metsDom, dipUuid, outputDipDir, filesInObjectDirectory):
    dmdSec = getDmdSec(metsDom)
    dcMetadata = parseDcXml(dmdSec)

    outputDipDir = prepareOutputDir(outputDipDir, 'projectclient', dipUuid)
    
    for file in filesInObjectDirectory:
      # First, copy the file into the output directory.
      # shutil.copy(os.path.join(inputDipDir, 'objects', file), outputDipDir)
      shutil.copy(file, outputDipDir)
    # Then, write out a tab-delimited file containing the DC-mapped metadata, with 'Filename' as the last field.
    collectionFieldInfo = getContentdmCollectionFieldInfo(args.contentdmServer, args.targetCollection)
    # Write out the metadata file, with the first row containing the field labels and the second row
    # containing the values. Both rows needs to be in the order expressed in collectionFieldInfo['order'].
    # For each item in collectionFieldInfo['order'], query each mapping in collectionFieldInfo['mappings']
    # to find a matching 'nick'; if the nick is found, write the value in the dmdSec's element that matches
    # the mapping's key; if no matching mapping is found, write ''. The DIP filename (in this case, the
    # file variable defined above) needs to go in the last column.
    delimHeaderRow = []
    delimValuesRow = []
    for field in collectionFieldInfo['order']:
        for k, v in collectionFieldInfo['mappings'].iteritems():
            if field == v['nick']:
               # Append the field name to the header row.
               delimHeaderRow.append(v['name'])
               # Append the element value to the values row.
               if k in dcMetadata:
                   # In CONTENTdm, repeated values are joined with a semicolon.
                   joinedDcMetadataValues = '; '.join(dcMetadata[k])
                   # Rows can't contain new lines.
                   joinedDcMetadataValues = joinedDcMetadataValues.replace("\r","")
                   joinedDcMetadataValues = joinedDcMetadataValues.replace("\n","")
                   delimValuesRow.append(joinedDcMetadataValues)
               # Append a placeholder to keep the row intact.
               else:
                   delimValuesRow.append('')
    
    delimitedFile = open(os.path.join(outputDipDir, 'simple.txt'), "wb")
    writer = csv.writer(delimitedFile, delimiter='\t')
    delimHeaderRow.append('Filename') # Must contain 'Filename' in last position
    writer.writerow(delimHeaderRow) 
    head, tail = os.path.split(file)
    delimValuesRow.append(tail) # Must contain filename in last position
    writer.writerow(delimValuesRow)
    delimitedFile.close()

    zipProjectClientOutput(outputDipDir, dipUuid)
    # Delete the unzipped version of the DIP since we don't use it anyway.
    shutil.rmtree(outputDipDir)

def generateCompoundContentDMDirectUploadPackage(metsDom, dipUuid, outputDipDir, filesInObjectDirectory, filesInThumbnailDirectory):
    for file in filesInObjectDirectory:
      print file 
    #  Compound items - multiple files in the DIP objects directory, ordered by the METS structMap.
    #    Need to consult the structMap and write out a corresponding structure file. Also, for every file,
    #    copy the file, create an .icon, create a .desc file, plus create index.desc, index.cpd, index.full,
    #    and ready.txt.


# Generate a 'project client' package for a compound CONTENTdm item from the Archivematica DIP.
# This package will contain the object file and a delimited metadata file in a format suitable
# for importing into CONTENTdm using its Project Client.
def generateCompoundContentDMProjectClientPackage(metsDom, dipUuid, outputDipDir, filesInObjectDirectory):
    pp = pprint.PrettyPrinter(indent=4) # Remove after development.
    dmdSec = getDmdSec(metsDom)
    dcMetadata = parseDcXml(dmdSec)

    # Archivematica's stuctMap is always the first one; the user-submitted structMap
    # is always the second one. @todo: If the user-submitted structMap is present,
    # parse it for the SIP structure so we can use that structure in the CONTENTdm packages.
    structMapDom =  metsDom.getElementsByTagName('structMap')[0]
    structMapDict = parseStructMap(structMapDom, filesInObjectDirectory)

    outputDipDir = prepareOutputDir(outputDipDir, 'projectclient', dipUuid)

    # Create a 'scans' subdirectory in the output directory.
    scansDir = os.path.join(outputDipDir, 'scans')
    os.makedirs(scansDir)

    # Write out the metadata file, with the first row containing the field labels and the second row
    # containing the values. Both rows needs to be in the order expressed in collectionFieldInfo['order'].
    # For each item in collectionFieldInfo['order'], query each mapping in collectionFieldInfo['mappings']
    # to find a matching 'nick'; if the nick is found, write the value in the dmdSec's element that matches
    # the mapping's key; if no matching mapping is found, write ''. The DIP filename (in this case, the
    # file variable defined above) needs to go in the last column.
    collectionFieldInfo = getContentdmCollectionFieldInfo(args.contentdmServer, args.targetCollection)
    delimHeaderRow = []
    delimItemValuesRow = []
    for field in collectionFieldInfo['order']:
        for k, v in collectionFieldInfo['mappings'].iteritems():
            if field == v['nick']:
               # Append the field name to the header row.
               delimHeaderRow.append(v['name'])
               # Append the element value to the values row.
               if k in dcMetadata:
                   # In CONTENTdm, repeated values are joined with a semicolon.
                   joinedDcMetadataValues = '; '.join(dcMetadata[k])
                   # Rows can't contain new lines.
                   joinedDcMetadataValues = joinedDcMetadataValues.replace("\r","")
                   joinedDcMetadataValues = joinedDcMetadataValues.replace("\n","")
                   delimItemValuesRow.append(joinedDcMetadataValues)
               # Append a placeholder to keep the row intact.
               else:
                   delimItemValuesRow.append('')

    delimitedFile = open(os.path.join(outputDipDir, 'compound.txt'), "wb")
    writer = csv.writer(delimitedFile, delimiter='\t')
    # Write the header row.
    delimHeaderRow.append('Filename') # Must contain 'Filename' in last position
    writer.writerow(delimHeaderRow) 
    # Write the item-level metadata row.
    writer.writerow(delimItemValuesRow) 

    # Determine the order in which we will add the child-level rows to the delimited file.
    Orders = []
    for fptr, details in structMapDict.iteritems():
        Orders.append(details['order'])

    # Iterate through the list of order values and add the matching structMapDict entry
    # to the delimited file (and copy the file into the scans directory).
    for order in sorted(Orders):
        for k, v in structMapDict.iteritems():
            if order == v['order']:
               delimChildValuesRow = []
               # Find the full path of the file identified in v['filename'].
               for fullPath in filesInObjectDirectory:
                   if (v['filename'] in fullPath):
                       shutil.copy(fullPath, scansDir)
               # Write the child-level metadata row. @todo: For flat items with no child-level metadata,
               # we are using the label for the child as defined in structMapDict and the filename only.
               # This means that we put the label in the position allocated for the dc.title element,
               # and the filename in the last position. Everthing in between is ''. This will need to be
               # made more functional for flat with child-leve metadata, and for hierarchical.
               titlePosition = collectionFieldInfo['order'].index('title')
               if titlePosition == 0:
                   delimChildValuesRow.append(v['label'])
                   for i in range(1, len(delimHeaderRow) - 1):
                       delimChildValuesRow.append('')
               delimChildValuesRow.append(v['filename']) # Must contain filename in last position
               writer.writerow(delimChildValuesRow)

    delimitedFile.close()

    zipProjectClientOutput(outputDipDir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='restructure')
    parser.add_argument('--uuid', action="store", dest='uuid', metavar='UUID', help='SIP-UUID')
    parser.add_argument('--dipDir', action="store", dest='dipDir', metavar='dipDir', help='DIP Directory')
    parser.add_argument('--server', action="store", dest='contentdmServer', metavar='server', help='Target CONTENTdm server')
    parser.add_argument('--collection', action="store", dest='targetCollection',
                        metavar='targetCollection', help='Target CONTENTdm Collection')
    parser.add_argument('--ingestFormat', action="store", dest='ingestFormat', metavar='ingestFormat',
                        default='directupload', help='The format of the ingest package, either directupload or projectclient')
    parser.add_argument('--outputDir', action="store", dest='outputDir', metavar='outputDir',
                        help='The destination for the restructured DIPs')

    args = parser.parse_args()

    # Define the directory where DIPs are waiting to be processed.
    inputDipDir = args.dipDir
    # Use %watchDirectoryPath%uploadedDIPs as the output directory for the directupload and projectclient output.
    # We also create a 'CONTENTdm' subdirectory for DIPs created by this microservice.
    outputDipDir = os.path.join(args.outputDir, 'CONTENTdm')
    if not os.path.exists(outputDipDir):
        os.makedirs(outputDipDir)

    # Perform some preliminary validation on the argument values.
    if not os.path.exists(inputDipDir):
        print "Sorry, can't find " + inputDipDir
        sys.exit(1)

    if args.ingestFormat not in ['directupload', 'projectclient']:
        print "Sorry, ingestFormat must be either 'directupload' or 'projectclient'"
        sys.exit(1)

    # Read and parse the METS file. Assumes there is one METS file in the DIP directory.
    for infile in glob.glob(os.path.join(inputDipDir, "METS*.xml")):
        metsFile = infile
    metsDom = parse(metsFile)

    # Check to see if we're dealing with a simple or compound item, and fire the
    # appropriate DIP-generation function.
    filesInObjectDirectory = getObjectDirectoryFiles(os.path.join(inputDipDir, 'objects'))
    if os.path.exists(os.path.join(inputDipDir, 'thumbnails')):
        filesInThumbnailDirectory = glob.glob(os.path.join(inputDipDir, 'thumbnails', "*.jpg"))

    if len(filesInObjectDirectory) == 1 and args.ingestFormat == 'directupload':
        generateSimpleContentDMDirectUploadPackage(metsDom, args.uuid, outputDipDir, filesInObjectDirectory, filesInThumbnailDirectory)
    if len(filesInObjectDirectory) == 1 and args.ingestFormat == 'projectclient':
        generateSimpleContentDMProjectClientPackage(metsDom, args.uuid, outputDipDir, filesInObjectDirectory)

    if len(filesInObjectDirectory) > 1 and args.ingestFormat == 'directupload':
        generateCompoundContentDMDirectUploadPackage(metsDom, args.uuid, outputDipDir, filesInObjectDirectory, filesInThumbnailDirectory)
    if len(filesInObjectDirectory) > 1 and args.ingestFormat == 'projectclient':
        generateCompoundContentDMProjectClientPackage(metsDom, args.uuid, outputDipDir, filesInObjectDirectory)
