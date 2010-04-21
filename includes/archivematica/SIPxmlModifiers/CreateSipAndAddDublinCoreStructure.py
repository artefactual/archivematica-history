#!/usr/bin/python
#import xml.etree.cElementTree as etree
import xml.etree.ElementTree as etree



from datetime import datetime


root = etree.Element("SIP")
root.text = "\n\t"
dc = etree.Element("doublincore")
dc.text = "\n\t\t"
dc.tail = "\n"
root.append(dc)

title = etree.Element("Title")
dc.append(title)
title.text = " "
title.tail = "\n\t\t"

provenance = etree.Element("provenance")
dc.append(provenance)
provenance.text = " "
provenance.tail = "\n\t\t"

partOf = etree.Element("partOf")
dc.append(partOf)
partOf.text = " "
partOf.tail = "\n\t\t"

description = etree.Element("description")
dc.append(description)
description.text = " "
description.tail = "\n\t\t"

dateReceived = etree.Element("dateReceived")
dc.append(dateReceived)
dateReceived.text = (datetime.utcnow()).__str__()
dateReceived.tail = "\n\t"

# identifier

#print(etree.tostring(root, None, "xml", None, True, True, None))
print(etree.tostring(root))
tree = etree.ElementTree(root)
#tree.write(sys.argv[1]+"/SIP.xml")
tree.write("SIP.xml")

