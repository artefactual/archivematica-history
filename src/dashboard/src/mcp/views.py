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

from django.http import HttpResponse
from dashboard.contrib.mcp.client import MCPClient
from lxml import etree

def approve_job(request):
  result = ''
  if 'uuid' in request.REQUEST:
    client = MCPClient()
    uuid = request.REQUEST.get('uuid', '')
    result = client.approve_job(uuid)
  return HttpResponse(result, mimetype = 'text/plain')

def jobs_awaiting_approval(request):
  client = MCPClient()
  jobs = etree.XML(client.get_jobs_awaiting_approval())
  response = ''
  if 0 < len(jobs):
    for job in jobs:
      response += etree.tostring(job)
  response = '<Jobs>' + response + '</Jobs>'
  return HttpResponse(response, mimetype = 'text/xml')

def reject_job(request):
  result = ''
  if 'uuid' in request.REQUEST:
    client = MCPClient()
    uuid = request.REQUEST.get('uuid', '')
    result = client.reject_job(uuid)
  return HttpResponse(result, mimetype = 'text/plain')