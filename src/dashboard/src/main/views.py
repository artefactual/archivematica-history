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
import os, re, calendar, subprocess

def explore(request, uuid):
  # Database query
  job = Job.objects.get(jobuuid = uuid)
  # Prepare response object
  contents = []
  response = {}
  response['contents'] = contents
  # Parse request
  if 'path' in request.REQUEST and len(request.REQUEST['path']) > 0:
    directory = os.path.join(job.directory, request.REQUEST['path'])
    response['base'] = request.REQUEST['path'].replace('.', '')
  else:
    directory = job.directory
    response['base'] = ''
  # Build directory
  directory = os.path.abspath(directory)
  # Security check
  tmpDirectory = os.path.realpath(directory)
  while True:
    if tmpDirectory == os.path.realpath(job.directory):
      break
    elif tmpDirectory == '/':
      raise Http404
    else:
      tmpDirectory = os.path.dirname(tmpDirectory)
  # If it is a file, return the contents
  if os.path.isfile(directory):
    mime = subprocess.Popen('/usr/bin/file --mime-type ' + directory, shell=True, stdout=subprocess.PIPE).communicate()[0].split(' ')[-1].strip()
    response = HttpResponse(mimetype=mime)
    response['Content-Disposition'] = 'attachment; filename=%s' %  os.path.basename(directory)
    with open(directory) as resource:
      response.write(resource.read())
    return response
  # Cleaning path
  parentDir = os.path.dirname(directory)
  parentDir = parentDir.replace('%s/' % job.directory, '')
  parentDir = parentDir.replace('%s' % job.directory, '')
  response['parent'] = parentDir
  # Check if it is or not the root dir to add the "Go parent" link
  if os.path.realpath(directory) != os.path.realpath(job.directory):
    parent = {}
    parent['name'] = 'Go to parent directory...'
    parent['type'] = 'parent'
    contents.append(parent)
  # Add contents of the directory
  for item in os.listdir(directory):
    newItem = {}
    newItem['name'] = item
    if os.path.isdir(os.path.join(directory, item)):
      newItem['type'] = 'dir'
    else:
      newItem['type'] = 'file'
    contents.append(newItem)
  return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def sips(request, uuid=None):
  if request.method == 'GET':
    # Equivalent to: "SELECT SIPUUID, MAX(createdTime) AS latest FROM Jobs GROUP BY SIPUUID
    objects = Job.objects.filter(hidden=False).values('sipuuid').annotate(timestamp=Max('createdtime')).exclude(sipuuid__icontains = 'None')
    mcp_available = False
    try:
      client = MCPClient()
      jobsAwaitingApprovalXml = etree.XML(client.get_jobs_awaiting_approval())
      mcp_available = True
    except Exception: pass
    def encoder(obj):
      items = []
      for item in obj:
        jobs = get_jobs_by_sipuuid(item['sipuuid'])
        directory = jobs[0].directory
        item['directory'] = re.search(r'^.*/(?P<directory>.*)-[\w]{8}(-[\w]{4}){3}-[\w]{12}$', directory).group('directory')
        item['timestamp'] = calendar.timegm(item['timestamp'].timetuple())
        item['uuid'] = item['sipuuid']
        item['id'] = item['sipuuid']
        del item['sipuuid']
        item['jobs'] = []
        for job in jobs:
          newJob = {}
          item['jobs'].append(newJob)
          newJob['uuid'] = job.jobuuid
          newJob['microservice'] = map_known_values(job.jobtype)
          newJob['currentstep'] = map_known_values(job.currentstep)
          newJob['timestamp'] = '%d.%s' % (calendar.timegm(job.createdtime.timetuple()), str(job.createdtimedec).split('.')[-1])
          try: jobsAwaitingApprovalXml
          except NameError: pass
          else:
            for uuid in jobsAwaitingApprovalXml.findall('Job/UUID'):
              if uuid.text == job.jobuuid:
                newJob['status'] = 1
                break
        items.append(item)
      return items
    response = {}
    response['objects'] = objects
    response['mcp'] = mcp_available
    return HttpResponse(simplejson.JSONEncoder(default=encoder).encode(response), mimetype='application/json')
  elif request.method == 'DELETE':
    jobs = Job.objects.filter(sipuuid = uuid)
    try:
      client = MCPClient()
      jobsAwaitingApprovalXml = etree.XML(client.get_jobs_awaiting_approval())
      for uuid in jobsAwaitingApprovalXml.findall('Job/UUID'):
        if 0 < len(jobs.filter(jobuuid=uuid.text)):
          client.reject_job(uuid.text)
    except Exception: pass
    jobs.update(hidden=True)
    response = simplejson.JSONEncoder().encode({'removed': True})
    return HttpResponse(response, mimetype='application/json')

def tasks(request, uuid):
  job = Job.objects.get(jobuuid = uuid)
  objects = job.task_set.all().order_by('-createdtime')
  return render_to_response('main/tasks.html', locals())

def map_known_values(value):
  map = {
    # currentStep
    'completedSuccessfully': 'Completed successfully',
    'completedUnsuccessfully': 'Failed',
    'exeCommand': 'Executing command(s)',
    'verificationCommand': 'Executing command(s)',
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
    'Normalization Failed': 'Normalization failed',
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
  jobs = Job.objects.filter(sipuuid = uuid).order_by('-createdtime')
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