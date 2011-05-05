#!/usr/bin/python

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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage MCPrpcCLI
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import xmlrpclib
import lxml.etree as etree
import os

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

def updateclientInfo(clientInfo):
    del clientInfo
    ret = proxy.getClientInfo()
    clientInfo = etree.XML(ret)
    return clientInfo


if __name__ == '__main__':
    os.system("clear")
    clientInfo = etree.Element("clientInfo")
    clientInfo = updateclientInfo(clientInfo)
    #print etree.tostring(clientInfo)
    choice = "No-op"
    while choice != "q":
        print etree.tostring(clientInfo)
        print "q to quit"
        print "u to update List"
        choice = raw_input('Please enter a value:')
        os.system("clear")
        print "choice: " + choice
        clientInfo = updateclientInfo(clientInfo)
            
    
    



