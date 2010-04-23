#!/usr/bin/python
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

dc = findDirectory(root, "dublincore")
identifier = etree.Element("dcterms:provenance")
dc.append(identifier)
identifier.text = sys.argv[2].__str__()

tree.write(sys.argv[1]+"/SIP.xml")

