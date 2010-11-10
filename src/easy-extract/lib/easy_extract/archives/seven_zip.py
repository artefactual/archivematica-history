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


"""7zip archive format"""
import os
import re

from easy_extract.archive import Archive

RAW_EXTENSIONS = ['.ARJ', '.CAB', '.CHM', '.CPIO',
                  '.DMG', '.HFS', '.LZH', '.LZMA',
                  '.NSIS', '.UDF', '.WIM', '.XAR',
                  '.Z', '.ZIP', '.GZIP', '.TAR',]

EXTENSIONS = [re.compile('%s$' % ext, re.I) for ext in RAW_EXTENSIONS]

class SevenZipArchive(Archive):
    """The 7z unarchiver is used for many formats"""
    ALLOWED_EXTENSIONS = EXTENSIONS
    
    def _extract(self):
        first_archive = self.get_command_filename(self.archives[0])
        output_folder = self.get_extraction_path(self.archives[0])
        return not os.system('7z x -o%s ' % output_folder + first_archive)
        
    
