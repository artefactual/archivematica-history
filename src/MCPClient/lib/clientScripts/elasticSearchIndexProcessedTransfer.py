#!/usr/bin/python -OO

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
# @subpackage Ingest
# @author Mike Cantelon <mike@artefactual.com>
# @version svn: $Id$
import sys
import os
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
from pyes import *

exitCode = 0
pathToElasticSearchServer='/opt/elasticsearch/bin/elasticsearch'

def index_transfer(conn, uuid, pathToTransfer):
    filesIndexed = 0
    for filepath in list_files_in_dir(pathToTransfer):
        if os.path.isfile(filepath):
            print filepath
            print os.path.basename(filepath)
            filesIndexed = filesIndexed + 1
    # cycle through all files
    # store timestamp, relative filepath, extension, size
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

if __name__ == '__main__':
    pathToTransfer = sys.argv[1] + 'objects'
    transferUUID = sys.argv[2]

    # make sure elasticsearch is installed
    if (os.path.exists(pathToElasticSearchServer)):

        # make sure transfer files exist
        if (os.path.exists(pathToTransfer)): 
            conn = ES('127.0.0.1:9200')

            filesIndexed = index_transfer(conn, transferUUID, pathToTransfer)

            print 'Path to transfer objects: ' + pathToTransfer
            print 'Transfer UUID: ' + transferUUID
            print 'Files indexed: ' + str(filesIndexed)

        else:
            print >>sys.stderr, "Directory does not exist: ", pathToTransfer
            exitCode = 1
    else:
        print >>sys.stderr, "Elasticsearch not found, normally installed at ", pathToElasticSearchServer
        exitCode = 1

quit(exitCode)
