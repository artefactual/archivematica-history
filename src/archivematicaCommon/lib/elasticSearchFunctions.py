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

