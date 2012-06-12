#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

class replacementDic:
    def __init__(self, dictionary):
        self.dic = dictionary
    
    def replace(self, *a):
        ret = []
        for orig in a:
            new = orig
            if orig != None:
                for key, value in self.dic.iteritems():
                    orig = orig.replace(key, value)
            ret.append(orig)
        return ret


class choicesDic:
    def __init__(self, dictionary):
        self.dic = dictionary