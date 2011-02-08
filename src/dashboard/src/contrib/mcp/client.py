# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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

from django.conf import settings
from xmlrpclib import ServerProxy, Error
import socket

class MCPClient:

  def __init__(self, host = settings.MCP_SERVER[0], port = settings.MCP_SERVER[1]):
    self.url = 'http://%s:%d' % (host, port)
    self.server = ServerProxy(self.url)
    socket.setdefaulttimeout(3)

  def approve_job(self, uuid):
    return self.server.approveJob(uuid)

  def get_jobs_awaiting_approval(self):
    return self.server.getJobsAwaitingApproval()

  def reject_job(self, uuid):
    return self.server.rejectJob(uuid)