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

List of clients
List of jobs to queue
List of active jobs [UUID, folder to move when done.]

def loadFolderWatchLlist()
  Loads a config file with:
     folders and the associated next command to run 
     folder to move the files to while they will be operated on
     folder to move to when all tasks are completed
     whether it's a task for each file/file&folder/One task for the entire SIP
     specifies if the user needs to approve the next command, or if it's automatic.
  note: will need some watch folder functionality

def  MCPclient()
    request info:
      give info
    approveJob:
      add job to que
      
def clientConnect(client UUID, client nice name, connect back info)
  getIP/connection info
  connect back to client.(to issues commands to client)
  return configDic
  #connection terminates
  
def processQue
  While(1):
    take que task
    send task to available client, with taskCompleted() ret, and JobUUID., relative path the files can be found (relative to shared folder.
    
def taskCompleted(jobUUID):
  make note in the logs
  if the 



if __name__ == '__main__':
  folderWatchList = loadFolderWatchLlist()
  Start listening for client connections (new thread) 
  Start listening for MCPclient Connections.
  
  JOB UUID - operating on the entire SIP folder
  Task - A job can contain many tasks- a task is per file
  
