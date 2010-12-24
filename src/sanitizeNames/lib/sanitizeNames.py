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
# @subpackage sanitizeNames
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import string
import os
from shutil import move as rename
import sys

VERSION = "1.0." +  "$Rev$".replace(" $", "").replace("$Rev: ","")
valid = "-_.()" + string.ascii_letters + string.digits
replacementChar = "_"

def sanitizeName(basename):
    ret = ""
    for c in basename:
        if c in valid:
            ret += c
        else:
            ret += replacementChar
    return ret

def sanitizePath(path):
    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    sanitizedName = sanitizeName(basename)
    if 0:
        print "path: " + path
        print "dirname: " + dirname
        print "basename: " + basename
        print "sanitizedName: " + sanitizedName
        print "renamed:", basename != sanitizedName
    if basename == sanitizedName:
        return path
    else:
        n = 1
        s = sanitizedName
        fileTitle = s[:s.rfind('.')]
        fileExtension = s.split(".")[-1]
        if fileExtension != sanitizedName:
            fileExtension = "." + fileExtension
        else:
             fileExtension = ""
        sanitizedName = dirname + "/" + fileTitle + fileExtension
               
        while os.path.exists(sanitizedName):
            sanitizedName = dirname + "/" + fileTitle + replacementChar + n.__str__() + fileExtension
            n+=1 
        rename(path, sanitizedName)
        return sanitizedName
    
def sanitizeRecursively(path):
    sanitizedName = sanitizePath(path)
    if sanitizedName != path:
        print path + " -> " + sanitizedName
    if os.path.isdir(sanitizedName):
        for f in os.listdir(sanitizedName):
            sanitizeRecursively(sanitizedName + "/" + f)
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >>sys.stderr, "Error, sanitizeNames takes one agrument PATH or -V (version)"
        quit(-1)
    path = sys.argv[1]
    if path == "-V":
        print VERSION
        quit(0)
    if not os.path.isdir(path):
        print >>sys.stderr, "Not a directory: " + path
        quit(-1)
    path = os.path.abspath(path)
    print "Scanning: " + path
    sanitizeRecursively(path)
      
