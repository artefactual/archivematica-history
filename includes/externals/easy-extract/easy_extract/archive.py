#!/usr/bin/python
#http://pypi.python.org/pypi/easy-extract/0.1.0

#ORIGINAL DEVELOPER:
#  Author:  Fantomas42 <fantomas42@gmail.com>
# Home Page: http://fantomas.willbreak.it
# Keywords: extract,rar,zip,xtm
# License: GPL 



#MODIFIER DEVELOPER:
# @package Archivematica
# @subpackage easy_extract
# @author Joseph Perry <Joseph@artefactual.com>
# @version svn: $Id$
# Date March 9th 2010
# Organization: Artefactual Systems Inc.
# Home Page: http://artefactual.com
# Home Page: http://archivematica.org/
""" Modification Details:
Instead of extracting everything to one folder, create a folder with a unique name, based on the archive name and specific time.
Extract the archive within that folder.

Added -w option to look for archives within just extracted files.
"""

# License:  
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

"""Archive collection modules"""
import os
import re
import time

CHAR_TO_ESCAPE = (' ', '(', ')', '*', "'", '"', '&', '.')

class BaseFileCollection(object):
    """Base file collection"""

    def __init__(self, name, path='.', filenames=[]):
        self.name = name
        self.path = path
        self.filenames = filenames
        self.time = "-".join((str(time.time())).split('.')) #UTP time seperated by - instead of .
        
    def escape_filename(self, filename):
        """Escape a filename"""
        for char in CHAR_TO_ESCAPE:
            filename = filename.replace(char, '\%s' % char)
        return filename

    def get_path_filename(self, filename):
        """Concatenate path and filename"""
        return os.path.join(self.path, filename)

    def get_command_filename(self, filename):
        """Convert filename for command line"""
        return self.escape_filename(self.get_path_filename(filename))
    
    def get_extraction_path(self, filename):
        return self.escape_filename(self.path + "/" + filename + self.time + "/")
    
    def get_extraction_path_non_delim(self, filename):
        return self.path + "/" + filename + self.time + "/"
    #def get_absolute_path_filename(self, filename):
    #    return os.path.abspath(os.join(self.path, filename))

class MedKit(BaseFileCollection):
    """MedKit is collection of par2 files"""

    def __init__(self, name, path='.', filenames=[]):
        super(MedKit, self).__init__(name, path, filenames)
        self.medkits = []
        self.find_medkits(self.filenames)

    def is_medkit_file(self, filename):
        """Check if the filename is a medkit"""
        return bool(filename.startswith(self.name) and filename.lower().endswith('.par2'))

    def find_medkits(self, filenames=[]):
        """Find files for building the medkit"""
        for filename in filenames:
            if self.is_medkit_file(filename) and not filename in self.medkits:
                self.medkits.append(filename)
        self.medkits.sort()

    def check_and_repair(self, silent=False):
        """Check and repair with medkits"""
        if self.medkits:
            options = silent and '-qq' or ''            
            root_medkit = self.get_command_filename(self.medkits[0])
            result = os.system('par2 r %s %s' % (options, root_medkit))
            return bool(not result)
        return False

class Archive(MedKit):
    """Archive is a collection of archive files and a MedKit"""
    ALLOWED_EXTENSIONS = []

    def __init__(self, name, path='.', filenames=[]):
        super(Archive, self).__init__(name, path, filenames)
        self.archives = []
        self.find_archives(self.filenames)

    @property
    def files(self):
        return self.archives + self.medkits

    @classmethod 
    def is_archive_file(cls, filename):
        """Check if the filename is allowed for the Archive"""
        for regext in cls.ALLOWED_EXTENSIONS:
            if regext.search(filename):
                return regext.split(filename)[0]
        return False

    def find_archives(self, filenames=[]):
        """Find files for building the archive"""
        for filename in filenames:
            if filename.startswith(self.name) and self.is_archive_file(filename) \
                   and not filename in self.archives:
                self.archives.append(filename)
        self.archives.sort()

    def extract(self, repair=True):
        """Extract the archive and do integrity checking"""
        extraction = self._extract()

        if not extraction and repair:
            if self.check_and_repair():
                extraction = self._extract()
        return extraction

    def _extract(self):
        """Extract the archive"""
        raise NotImplementedError

    def __str__(self):
        return '%s (%i archives, %i par2 files)' % (self.name, len(self.archives),
                                                    len(self.medkits))

