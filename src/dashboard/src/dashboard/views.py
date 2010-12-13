from django.db.models import Max
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError

from dashboard.contrib.mcp.client import MCPClient
from dashboard.dashboard.models import Task, Job
from lxml import etree

import os

def sips(request):
  # Equivalent to: "SELECT SIPUUID, MAX(createdTime) AS latest FROM Jobs GROUP BY SIPUUID
  objects = Job.objects.values('sipuuid').annotate(latest = Max('createdtime')).order_by('-latest').exclude(sipuuid__icontains = 'None')
  return render_to_response('sips.html', locals())

def show_dir(request, jobuuid):
  try:
    job = Job.objects.get(jobuuid = jobuuid)
    list = os.listdir(job.directory)
    return render_to_response('show_dir.html', locals())
  except Exception: raise Http404

def show_subdir(request, jobuuid, subdir):
  try:
    job = Job.objects.get(jobuuid = jobuuid)
    path = os.path.join(job.directory, subdir)
    if (os.path.isfile(path)):
      from django.utils.encoding import smart_str
      response = HttpResponse(mimetype = 'application/force-download')
      response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path)
      response['X-Sendfile'] = smart_str(path)
      response['Content-Type'] = ''
      response['Content-Length'] = os.stat(path).st_size
      # It's usually a good idea to set the 'Content-Length' header too.
      # You can also set any other required headers: Cache-Control, etc.
      return response
    else:
      parent = path.replace(job.directory, '')
      list = os.listdir(path)
      return render_to_response('show_dir.html', locals())
  except Exception: raise Http404

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
  return HttpResponseRedirect(reverse(sips))

def tasks(request, page = 1):
  if 'jobuuid' in request.REQUEST:
    job = Job.objects.get(jobuuid = request.REQUEST.get('jobuuid'))
    objects = job.task_set.all()
  else:
    objects = Task.objects.all().order_by('-createdtime')
  paginator = Paginator(objects, 10)

  try:
    objects = paginator.page(page)
  except (EmptyPage, InvalidPage):
    objects = paginator.page(paginator.num_pages)

  return render_to_response('tasks.html', locals())