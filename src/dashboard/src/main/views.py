from django.db.models import Max
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from dashboard.main.models import Task, Job
from django.utils import simplejson
import os
import re

def show_dir(request, jobuuid):
  try:
    job = Job.objects.get(jobuuid = jobuuid)
    list = os.listdir(job.directory)
    return render_to_response('main/show_dir.html', locals())
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
      return render_to_response('main/show_dir.html', locals())
  except Exception: raise Http404

def get_all(request):
  # Equivalent to: "SELECT SIPUUID, MAX(createdTime) AS latest FROM Jobs GROUP BY SIPUUID
  objects = Job.objects.values('sipuuid').annotate(timestamp = Max('createdtime')).order_by('-timestamp').exclude(sipuuid__icontains = 'None')
  def encoder(obj):
    items = []
    for item in obj:
      item['directory'] = get_directory_by_sipuuid(item['sipuuid'])
      item['timestamp'] = item['timestamp'].strftime('%x %X')
      item['uuid'] = item['sipuuid']
      del item['sipuuid']
      items.append(item)
    return items
  response = simplejson.JSONEncoder(default=encoder).encode(objects)
  return HttpResponse(response, mimetype='application/json')

def get_directory_by_sipuuid(value):
  directory = Job.objects.filter(sipuuid = value)[0].directory
  return re.search(r'^.*/(?P<directory>.*)-[\w]{8}(-[\w]{4}){3}-[\w]{12}$', directory).group('directory')