#!/usr/bin/python
#

import os
import uuid
from xml.sax.saxutils import quoteattr as xml_quoteattr

path = "/home/demo/"

def DirAsLessXML(path):
    result = '  <dir name=%s ' % xml_quoteattr(os.path.basename(path)) 
    result += 'original_name=%s>\n' % xml_quoteattr(os.path.basename(path))
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isdir(itempath):
            result += '\n'.join('  ' + line for line in 
                DirAsLessXML(os.path.join(path, item)).split('\n'))
        elif os.path.isfile(itempath):
            myuuid = uuid.uuid4()
            result += '    <file>\n'
            result += '       <name>%s</name>\n' % ''.join(xml_quoteattr(item).split("\"")[1:-1])
            result += '       <original_name>%s</original_name>\n' % ''.join(xml_quoteattr(item).split("\"")[1:-1])
            result += '       <UUID>%s</UUID>\n' % (myuuid)
            result += '    </file>\n'
    result += '  </dir>\n'
    return result

if __name__ == '__main__':
    print '<sipname>\n' + DirAsLessXML(os.getcwd()) + '</sipname>'
