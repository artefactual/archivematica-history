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


def doTask(task - parameters) #called from server
  switch(task)
    verifyChecksum
    extractPackage
    assign identifier
    cleanFilename
    checkForVirus
    identifyFormat
    validateFormat
    extractMetadata
    gatherMetadata
    normalizeFile
    createPackage
    storeAIP?
    
    


if __name__ == '__main__':
  connect to server
  send client info
  wait for server to connect
  
  
