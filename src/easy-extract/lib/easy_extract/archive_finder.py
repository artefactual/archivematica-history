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

"""Find and build the archives"""
import os


class ArchiveFinder(object):
    """Find and build the archives contained in path"""

    def __init__(self, paths=['.'], recursive=True, archive_classes=[]):
        if isinstance(paths, basestring):
            paths = [paths]
        self.paths = paths
        self.recursive = recursive
        self.archive_classes = archive_classes
        self.path_archives_found = self.find_archives(self.paths,
                                                      self.recursive,
                                                      self.archive_classes)

    def is_archive_file(self, filename, archive_classes=[]):
        """Check if the filename is associated to an
        archive class"""
        for archive_class in archive_classes:
            archive_name = archive_class.is_archive_file(filename)
            if archive_name:
                return archive_name, archive_class
        return False, False

    def get_path_archives(self, path, filenames=[], archive_classes=[]):
        """Build and return Archives list from a path"""
        archives = {}
            
        for filename in filenames:
            name, archive_class = self.is_archive_file(filename, archive_classes)
            
            if archive_class and not name in archives.keys():
                archives[name] = archive_class(name, path, filenames)

        return archives.values()

    def find_archives(self, paths, recursive, archive_classes=[]):
        """Walk to the paths finding archives"""
        path_archives = {}
        print "paths: "
        print paths

        for path in paths:
            for (dirpath, dirnames, filenames) in os.walk(path):
                path_archives[dirpath] = self.get_path_archives(dirpath, filenames,
                                                                archive_classes)
                if not recursive:
                    break
                
        return path_archives

    @property
    def archives(self):
        """Return all Archives found"""
        archives = []
        for ars in self.path_archives_found.values():
            archives.extend(ars)
        return archives

