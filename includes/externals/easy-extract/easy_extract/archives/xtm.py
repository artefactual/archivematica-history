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

"""Xtm archive format"""
import os
import re

from easy_extract.archive import Archive

EXTENSIONS = [re.compile('.\d{3}.xtm$', re.I),
              re.compile('.xtm$', re.I)]

class XtmArchive(Archive):
    """The XTM archive format"""
    ALLOWED_EXTENSIONS = EXTENSIONS

    def _extract(self):
        new_directory_name = self.get_extraction_path(self.archives[0])
        new_filename =  new_directory_name + self.escape_filename(self.remove_xtm_from_filename(self.archives[0]))
        first_archive = self.get_command_filename(self.archives[0])
        
        
        
        os.system('mkdir %s' % new_directory_name)
        os.system('dd if=%s skip=1 ibs=104 status=noxfer > %s 2>/dev/null' % \
                  (first_archive, new_filename))
        
        for archive in self.archives[1:]:
            archive = self.get_command_filename(archive)
            os.system('cat %s >> %s' % (archive, new_filename))

        return True
        # Need to return value
        
        
    def remove_xtm_from_filename(self,filename):        
        for regext in self.ALLOWED_EXTENSIONS:
            if regext.search(filename):
                return regext.split(filename)[0]

        
