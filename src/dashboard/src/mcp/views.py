from django.conf import settings
from django.http import HttpResponse

from dashboard.contrib.mcp.client import MCPClient
from lxml import etree

def approve_job(request):
  result = ''
  if 'uuid' in request.REQUEST:
    client = MCPClient(settings.MCP_SERVER[0], settings.MCP_SERVER[1])
    uuid = request.REQUEST.get('uuid', '')
    result = client.approve_job(uuid)
  return HttpResponse(result, mimetype = 'text/plain')

def jobs_awaiting_approval(request):
  client = MCPClient(settings.MCP_SERVER[0], settings.MCP_SERVER[1])
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
    client = MCPClient(settings.MCP_SERVER[0], settings.MCP_SERVER[1])
    uuid = request.REQUEST.get('uuid', '')
    result = client.reject_job(uuid)
  return HttpResponse(result, mimetype = 'text/plain')