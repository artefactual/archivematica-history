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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage archivematicaCommon
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import _mysql
import os
import threading
import MySQLdb
import string
from datetime import datetime

global separator
separator = "', '"

def getUTCDate():    
    """Returns a string of the UTC date & time in ISO format"""
    d = datetime.utcnow()
    return d.isoformat('T')

def getDeciDate(date):
    valid = "." + string.digits
    ret = ""
    for c in date:
        if c in valid:
            ret += c
        #else:
            #ret += replacementChar
    return ret


#sudo apt-get install python-mysqldb
sqlLock = threading.Lock()
sqlLock.acquire()
global database
database=MySQLdb.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
sqlLock.release()

def runSQL(sql):
    global database
    print sql
    #found that even though it says it's compiled thread safe, running it multi-threaded crashes it.
    sqlLock.acquire()
    db = database
    try:
        db.query(sql)
    except MySQLdb.OperationalError, message:  
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=_mysql.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
            sqlLock.release()
            runSQL(sql)
            return 
    sqlLock.release()
    return

def querySQL(sql):
    global database
    sqlLock.acquire()
    print sql
    try:
        c=database.cursor()
        c.execute(sql)
    except MySQLdb.OperationalError, message:  
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=_mysql.connect(db="MCP", read_default_file="/etc/archivematica/MCPServer/dbsettings")
            sqlLock.release()
            c=database.cursor()
            c.execute(sql)
    return c, sqlLock 
#        row = c.fetchone()
#        while row != None:
#            fileUUID = row[0]
#            filesToChecksum.append(row[0])
#            row = c.fetchone()
        





    
