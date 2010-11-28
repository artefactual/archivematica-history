from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from dashboard.dashboard.models import Task, Job

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
