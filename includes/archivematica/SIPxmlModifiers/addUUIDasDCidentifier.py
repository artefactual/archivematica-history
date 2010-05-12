#!/usr/bin/python
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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import sys
import xml.etree.cElementTree as etree

def findDirectory(root, tag=None, text=None):
	ret = []
	if (not tag) and (not text):
		#return all
		for element in root:
			ret.append(element)
	else:
		if tag:
			if not text:
				#match the tag
				for element in root:
					if element.tag == tag:
						ret.append(element)
			else:
				#match tag and text
				for element in root:
					if element.tag == tag and element.text == text:
						ret.append(element)
		else:
			#match the text
			for element in root:
				if element.text == text:
					ret.append(element)
	return ret
	
tree = etree.parse(sys.argv[1]+"/SIP.xml")
root = tree.getroot()


dc = findDirectory(root, "{http://archivematica.org/}dublincore")
identifier = etree.Element("{http://purl.org/dc/elements/1.1/}identifier")
dc[0].append(identifier)
identifier.text = sys.argv[2].__str__()


tree.write(sys.argv[1]+"/SIP.xml")

