#!/usr/bin/python
#

import os
import uuid
from xml.sax.saxutils import quoteattr as xml_quoteattr

path = "/home/demo/"

def DirAsLessXML(path):
    result = '  <dir name=%s>\n' % xml_quoteattr(os.path.basename(path))
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        if os.path.isdir(itempath):
            result += '\n'.join('  ' + line for line in 
                DirAsLessXML(os.path.join(path, item)).split('\n'))
        elif os.path.isfile(itempath):
            myuuid = uuid.uuid4()
            result += '    <filename>\n'
            result += '      <previous>%s</previous>\n' % xml_quoteattr(item)
            result += '      <UUID>%s</UUID>\n' % (myuuid)
            result += '    </filename>\n'
    result += '  </dir>\n'
    return result

if __name__ == '__main__':
    print '<sipname>\n' + DirAsLessXML(os.getcwd()) + '</sipname>'
