#!/usr/bin/env python
#modified from  http://ubuntuforums.org/showthread.php?t=926797

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

try:
    import sys
    import gtk, pygtk, os, os.path, pynotify
    pygtk.require('2.0')
except:
    print "Error: need python-notify, python-gtk2 and gtk"

def display(title, content):
  if not pynotify.init("Timekpr notification"):
    sys.exit(1)

  n = pynotify.Notification(title, content)
  #n = pynotify.Notification("Moo title", "test", "file:///path/to/icon.png")
  #n.set_urgency(pynotify.URGENCY_CRITICAL)
#  n.set_timeout(1) #milliseconds
#  n.set_category("device")

  #Call an icon
  #helper = gtk.Button()
  #icon = helper.render_icon(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_DIALOG)
  #n.set_icon_from_pixbuf(icon)

  if not n.show():
    print "Failed to send notification"
    sys.exit(1)


if __name__ == '__main__':
  display(sys.argv[1], sys.argv[2])


