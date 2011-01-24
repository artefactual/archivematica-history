from django.db.models import Max
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.utils import simplejson
from dashboard.contrib.mcp.client import MCPClient
from dashboard.main.models import Task, Job
from lxml import etree
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
  try:
    client = MCPClient()
    jobsAwaitingApprovalXml = etree.XML(client.get_jobs_awaiting_approval())
  except Exception: pass
  def encoder(obj):
    items = []
    for item in obj:
      jobs = get_jobs_by_sipuuid(item['sipuuid'])
      directory = jobs[0].directory
      item['directory'] = re.search(r'^.*/(?P<directory>.*)-[\w]{8}(-[\w]{4}){3}-[\w]{12}$', directory).group('directory')
      item['timestamp'] = item['timestamp'].strftime('%x %X')
      item['uuid'] = item['sipuuid']
      del item['sipuuid']
      item['jobs'] = []
      for job in jobs:
        newJob = {}
        item['jobs'].append(newJob)
        newJob['uuid'] = job.jobuuid
        newJob['microservice'] = map_known_values(job.jobtype)
        newJob['currentstep'] = map_known_values(job.currentstep)
        try: jobsAwaitingApprovalXml
        except NameError: pass
        else:
          for uuid in jobsAwaitingApprovalXml.findall('Job/UUID'):
            if uuid.text == job.jobuuid:
              newJob['status'] = 1
              break
      items.append(item)
    return items
  response = simplejson.JSONEncoder(default=encoder).encode(objects)
  return HttpResponse(response, mimetype='application/json')

def map_known_values(value):
  map = {
    # currentStep
    'completedSuccessfully': 'Completed successfully',
    'completedUnsuccessfully': 'Failed',
    'exeCommand': 'Executing',
    'requiresAprroval': 'Requires approval',
    'requiresApproval': 'Requires approval',
    # jobType
    'acquireSIP': 'Acquire SIP',
    'addDCToMETS': 'Add DC to METS',
    'appraiseSIP': 'Appraise SIP',
    'assignSIPUUID': 'Asign SIP UUID',
    'assignUUID': 'Assign file UUIDs and checksums',
    'bagit': 'Bagit',
    'cleanupAIPPostBagit': 'Cleanup AIP post bagit',
    'compileMETS': 'Compile METS',
    'copyMETSToDIP': 'Copy METS to DIP',
    'createAIPChecksum': 'Create AIP checksum',
    'createDIPDirectory': 'Create DIP directory',
    'createOrMoveDC': 'Create or move DC',
    'createSIPBackup': 'Create SIP backup',
    'detoxFileNames': 'Detox filenames',
    'extractPackage': 'Extract package',
    'FITS': 'FITS',
    'normalize': 'Normalize',
    'quarantine': 'Place in quarantine',
    'reviewSIP': 'Review SIP',
    'scanForRemovedFilesPostAppraiseSIPForPreservation': 'Scan for removed files post appraise SIP for preservation',
    'scanForRemovedFilesPostAppraiseSIPForSubmission': 'Scan for removed files post appraise SIP for submission',
    'scanWithClamAV': 'Scan with ClamAV',
    'seperateDIP': 'Seperate DIP',
    'storeAIP': 'Store AIP',
    'unquarantine': 'Remove from Quarantine',
    'uploadDIP': 'Upload DIP',
    'verifyChecksum': 'Verify checksum',
    'verifyMetadataDirectoryChecksums': 'Verify metadata directory checksums',
    'verifySIPCompliance': 'Verify SIP compliance',
  }
  if value in map:
    return map[value]
  else:
    return value

def get_jobs_by_sipuuid(uuid):
  jobs = Job.objects.all().filter(sipuuid = uuid).order_by('-createdtime')
  priorities = {
    'completedUnsuccessfully': 0,
    'requiresAprroval': 1,
    'requiresApproval': 1,
    'exeCommand': 2,
    'verificationCommand': 3,
    'completedSuccessfully': 4,
    'cleanupSuccessfulCommand': 5,
  }
  def get_priority(job):
    try: return priorities[job.currentstep]
    except Exception: return 0
  return sorted(jobs, key = get_priority) # key = lambda job: priorities[job.currentstep]