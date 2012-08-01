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
# @author Mike Cantelon <mike@artefactual.com>
# @version svn: $Id$

import time
import os

import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
import pyes
import xmltodict
import xml.etree.ElementTree as ElementTree

pathToElasticSearchServerFile='/etc/elasticsearch/elasticsearch.yml'

def connect_and_index(index, type, uuid, pathToTransfer):

    exitCode = 0

    # make sure elasticsearch is installed
    if (os.path.exists(pathToElasticSearchServerFile)):

        # make sure transfer files exist
        if (os.path.exists(pathToTransfer)):
            conn = pyes.ES('127.0.0.1:9200')
            try:
                conn.create_index(index)
            except pyes.exceptions.IndexAlreadyExistsException:
                pass

            # use METS file if indexing an AIP
            metsFilePath = os.path.join(pathToTransfer, 'METS.' + uuid + '.xml')

            if os.path.isfile(metsFilePath):
                filesIndexed = index_mets_file_metadata(
                    conn,
                    uuid,
                    metsFilePath,
                    index,
                    type
                )

            else:
                filesIndexed = index_directory_files(
                    conn,
                    uuid,
                    pathToTransfer,
                    index,
                    type
                )

            print type + ' UUID: ' + uuid
            print 'Files indexed: ' + str(filesIndexed)

        else:
            print >>sys.stderr, "Directory does not exist: ", pathToTransfer
            exitCode = 1
    else:
        print >>sys.stderr, "Elasticsearch not found, normally installed at ", pathToElasticSearchServerFile
        exitCode = 1

    return exitCode

def index_mets_file_metadata(conn, uuid, metsFilePath, index, type):
    filesIndexed     = 0
    filePathAmdIDs   = {}
    filePathMetsData = {}

    # establish structure to be indexed for each file item
    fileData = {
      'AIPUUID':   uuid,
      'indexedAt': time.time(),
      'filePath':  '',
      'METS':      {}
    }

    # parse XML
    tree = ElementTree.parse(metsFilePath)
    root = tree.getroot()

    # get amdSec IDs for each filepath
    for item in root.findall("{http://www.loc.gov/METS/}fileSec/{http://www.loc.gov/METS/}fileGrp/{http://www.loc.gov/METS/}file"):
        for item2 in item.findall("{http://www.loc.gov/METS/}FLocat"):
            filePath = item2.attrib['{http://www.w3.org/1999/xlink}href']
            filePathAmdIDs[filePath] = item.attrib['ADMID']

    # for each filepath, get data and convert to dictionary then index everything in the appropriate amdSec element
    for filePath in filePathAmdIDs:
        filesIndexed = filesIndexed + 1
        items = root.findall("{http://www.loc.gov/METS/}amdSec[@ID='" + filePathAmdIDs[filePath] + "']")
        for item in items:
            if item != None:
                xml = ElementTree.tostring(item)

                # set up data for indexing
                indexData = fileData
                indexData['filePath'] = filePath
                indexData['METS'] = xmltodict.parse(xml)

                # index data
                conn.index(indexData, index, type)

    print 'Indexed AIP files and corresponding METS XML.'

    return filesIndexed

def index_directory_files(conn, uuid, pathToTransfer, index, type):
    filesIndexed = 0

    # document structure
    transferData = {
      'uuid': uuid,
      'created': time.time()
    }

    # compile file data (relative filepath, extension, size)
    fileData = {}
    for filepath in list_files_in_dir(pathToTransfer):
        if os.path.isfile(filepath):
            fileData[filepath] = {
              'basename': os.path.basename(filepath)
            }
            filesIndexed = filesIndexed + 1

    transferData['filepaths'] = fileData

    # add document to index
    conn.index(transferData, index, type)

    return filesIndexed

def list_files_in_dir(path, filepaths=[]):
    # define entries
    for file in os.listdir(path):
        child_path = os.path.join(path, file)
        filepaths.append(child_path)

        # if entry is a directory, recurse
        if os.path.isdir(child_path) and os.access(child_path, os.R_OK):
            list_files_in_dir(child_path, filepaths)

    # return fully traversed data
    return filepaths

