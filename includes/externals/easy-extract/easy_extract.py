#!/usr/bin/python
#http://pypi.python.org/pypi/easy-extract/0.1.0

#ORIGINAL DEVELOPER:
#  Author:  Fantomas42 <fantomas42@gmail.com>
# Home Page: http://fantomas.willbreak.it
# Keywords: extract,rar,zip,xtm
# License: GPL 

#Tabified: no tabs, indent is 4 spaces


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






import sys, os
from optparse import OptionParser

from easy_extract import VERSION
from easy_extract.archives.xtm import XtmArchive
from easy_extract.archives.rar import RarArchive
from easy_extract.archives.seven_zip import SevenZipArchive
from easy_extract.archive_finder import ArchiveFinder

class EasyExtract(ArchiveFinder):
    """User interface for extracting archives"""

    def __init__(self, paths, recursive=False,
                 force_extract=False, repair=True, within=False ):
        self.force_extract = force_extract
        self.repair = repair
        self.excludes = []
        self.within = within

        super(EasyExtract, self).__init__( paths, recursive,
                                          [RarArchive, SevenZipArchive, XtmArchive,])

        if self.can_extract(self.force_extract):
            self.extract_archives(self.repair)
        else:
            print 'Nothing to do !'

    def get_path_archives(self, path, filenames, archive_classes):
        print 'Scanning %s...' % os.path.abspath(path)
        archives = super(EasyExtract, self).get_path_archives(
              path, filenames, archive_classes)
        return archives

    def can_extract(self, force):
        if self.archives:
            if force: return True
            for archive in self.archives:
                print archive
            extract = raw_input('Extract all ? [Y]es / No / Select : ')
            if not extract or 'y' in extract.lower():
                return True
            if 's' in extract.lower():
                for archive in self.archives:
                    extract = raw_input('Extract %s ? [Y]es / No : ' % archive)
                    if extract and not 'y' in extract.lower():
                        self.excludes.append(archive)
                return bool(self.archives)
        return False

    def extract_archives(self, repair):
        for archive in self.archives:
            if archive not in self.excludes:
                if not archive.extract(repair):
                    print "error extracting!!!"
                else: 
                    if self.within:
                        print "looking internal to just extracted archive"
                        directorie = archive.get_extraction_path_non_delim(archive.archives[0])
                        EasyExtract([directorie],
                            self.recursive,\
                            self.force_extract,\
                            self.repair,\
                            self.within)

if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options] [directory]...',
                          version='%prog ' + VERSION)
    parser.add_option('-f', '--force', dest='force_extract', action='store_true',
                      help='Do not prompt confirmation message', default=False)
    parser.add_option('-n', '--not-repair', dest='repair', action='store_false',
                      help='Do not try to repair archives on errors', default=True)
    parser.add_option('-r', '--recursive', dest='recursive', action='store_true',
                      help='Find archives recursively', default=False)
    parser.add_option('-w', '--within', dest='within', action='store_true',
                      help='Unzip archives within extracted archives', default=False)

    (options, args) = parser.parse_args()

    directories = ['.']
    if len(args):
        directories = args

    print '--** Easy Extract v%s **--' % VERSION
    EasyExtract(directories, options.recursive,
                options.force_extract, options.repair, options.within)
                
