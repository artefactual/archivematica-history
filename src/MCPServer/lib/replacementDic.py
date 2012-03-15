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

#testing
if __name__ == '__main__':
    rd = {"a":"A", "b":"B"}
    ins1 = "abcd"
    ins2 = "efga"
    ins3 = "a"
    ins4 = None
    ins5 = "seven"   
    a = replacementDic(rd)
    out = a.replace(ins1, ins2, ins3, ins4, ins5)
    print rd
    print ins1, ins2, ins3, ins4, ins5
    print out 