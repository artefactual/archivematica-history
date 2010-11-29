from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect

from dashboard.contrib.mcp.client import MCPClient
from dashboard.dashboard.models import Task, Job
from lxml import etree

def client(request):

  return render_to_response('client.html')

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

def index(request):

  return HttpResponseRedirect(reverse(jobs))

def jobs(request, page = 1):

  objects = Job.objects.all().order_by('-createdtime')

  paginator = Paginator(objects, 10)

  try:
    objects = paginator.page(page)
  except (EmptyPage, InvalidPage):
    objects = paginator.page(paginator.num_pages)

  return render_to_response('jobs.html', locals())

def tasks(request, page = 1):

  objects = Task.objects.all().order_by('-createdtime')

  paginator = Paginator(objects, 10)

  try:
    objects = paginator.page(page)
  except (EmptyPage, InvalidPage):
    objects = paginator.page(paginator.num_pages)

  return render_to_response('tasks.html', locals())
