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

#open
detox_fh = open(sys.argv[1]+"/filenameCleanup.log", "r")
tree = etree.parse(sys.argv[1]+"/SIP.xml")
root = tree.getroot()


#read first line & find uuid
line = detox_fh.readline()
if not line:
	print "error file empty or failed to open"
else:
	print "UUID: ",
	line = line.strip()
	uuid = line.split("/tmp/")
	print uuid[1]
	#if argv[1] != uuid or root.tag != uuid
		#error mismatched logs
		

#... now have the proper folder lined up with xml
#Each line is a list to process.

UUIDitem = findDirectory(root, "dir")
UUIDitem[0].set("originalName", sys.argv[2].split("/")[-1])

line = detox_fh.readline()
while line:
	detoxfiles = line.split(" -> ")
	oldfile = detoxfiles[0].split("/tmp",1)
	of = (oldfile[1].split("/"))
	branch = root	

	for folder in of[1:]:
		current_branch = branch

		#get the list of folders & find matching name
		dirs = findDirectory(branch, "dir")
		for directory in dirs:
			if directory.get("name") == folder:
				branch = directory
				break

		#if the branch has changed.
		if current_branch != branch:
			#if the log indicates the folder name changed:
			if folder == of[-1]:
				#modify branch to add old name
				branch.set("name", (detoxfiles[1].split("/")[-1]).split("\n")[0])
			continue

		else:
			#it may be a file
			if folder == of[-1]:
				files = findDirectory(branch, "file")
				for fil in files:				
					fi = findDirectory(fil, "name" , folder)
					if fi and len(fi) == 1:
						fi[0].text= (detoxfiles[1].split("/")[-1]).split("\n")[0]
					else:
						"error - logs don't correspond"

			else:
				print "error - logs don't correspond2"
				print folder
				print of
	
	line = detox_fh.readline()


tree.write(sys.argv[1]+"/SIP.xml")
     

