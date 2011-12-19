#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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
# @subpackage archivematicaCommon
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import MySQLdb
import os
import threading
import string
import sys
from datetime import datetime

global separator
separator = "', '"

#DB_CONNECTION_OPTS = dict(db="MCP", read_default_file="/etc/archivematica/archivematicaCommon/dbsettings")
DB_CONNECTION_OPTS = dict(db="MCP", read_default_file="/etc/archivematica/archivematicaCommon/dbsettings", charset="utf8", use_unicode = True)


def getSeparator():
    global separator
    return separator

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
database=MySQLdb.connect(**DB_CONNECTION_OPTS)
sqlLock.release()

def runSQL(sql):
    #print type(sql), sql
    if isinstance(sql, unicode):
        sql = sql.encode('utf-8')
    #print type(sql), sql
    global database
    #found that even though it says it's compiled thread safe, running it multi-threaded crashes it.
    sqlLock.acquire()
    db = database
    try:
        db.query(sql)
    except MySQLdb.OperationalError, message:
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=MySQLdb.connect(**DB_CONNECTION_OPTS)
            sqlLock.release()
            runSQL(sql)
            return
        else:
            print >>sys.stderr, "Error with query: ", sql
            print >>sys.stderr, "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
            exit(-100)
    sqlLock.release()
    return




def querySQL(sql):
    global database
    if isinstance(sql, unicode):
        sql = sql.encode('utf-8')
    sqlLock.acquire()
    print sql
    try:
        c=database.cursor()
        c.execute(sql)
    except MySQLdb.OperationalError, message:
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=MySQLdb.connect(**DB_CONNECTION_OPTS)
            import time
            time.sleep(10)
            c=database.cursor()
            c.execute(sql)
    return c, sqlLock
#        row = c.fetchone()
#        while row != None:
#            fileUUID = row[0]
#            filesToChecksum.append(row[0])
#            row = c.fetchone()


def queryAllSQL(sql):
    global database
    if isinstance(sql, unicode):
        sql = sql.encode('utf-8')
    sqlLock.acquire()
    #print sql
    rows = []
    try:
        c=database.cursor()
        c.execute(sql)
        rows = c.fetchall()
        sqlLock.release()
    except MySQLdb.OperationalError, message:
        #errorMessage = "Error %d:\n%s" % (message[ 0 ], message[ 1 ] )
        if message[0] == 2006 and message[1] == 'MySQL server has gone away':
            database=MySQLdb.connect(**DB_CONNECTION_OPTS)
            import time
            time.sleep(10)
            c=database.cursor()
            c.execute(sql)
            rows = c.fetchall()
            sqlLock.release()
    return rows
