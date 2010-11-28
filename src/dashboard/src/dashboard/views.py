from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect

from dashboard.dashboard.models import Task, Job

def client(request):

  return render_to_response('client.html')

def approve_job(request):

  return HttpResponse('', mimetype = 'text/plain')

def jobs_awaiting_approval(request):

  from dashboard.contrib.mcp.client import MCPClient
  from lxml import etree

  client = MCPClient()

  jobs = etree.XML(client.get_jobs_awaiting_approval())

  if 0 < len(jobs):

    response = ''

    for job in etree.XML(jobs):
      response += etree.tostring(job, pretty_print = True)

  else:

    response = 'There are not jobs awaiting for approval.'

  return HttpResponse(response, mimetype = 'text/plain')

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
