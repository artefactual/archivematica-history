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

from django.db.models import Max
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection, transaction
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.utils import simplejson
from dashboard.contrib.mcp.client import MCPClient
from dashboard.main.models import Task, Job
from lxml import etree
import calendar, os, re, simplejson, subprocess
from datetime import datetime

def manual_normalization(request, uuid):
  job = Job.objects.get(jobuuid=uuid)

  try:
    changes = simplejson.loads(request.POST.get('changes'))
  except TypeError:
    raise Http404

  # TODO: check input
  # name, newName and directory

  output = []
  returncodes = []
  for item in changes:

    if item["filename"].startswith('/'):
      item["filename"] = item["filename"][1:]

    if item["newFilename"].startswith('/'):
      item["newFilename"] = item["newFilename"][1:]

    command = []
    command.append("/usr/lib/archivematica/transcoder/premisXMLlinker.py")
    command.append("%s/objects/%s" % (job.directory, item["filename"]))
    command.append("%s/objects/%s" % (job.directory, item["newFilename"]))
    command.append("%s/" % job.directory)
    command.append("%s" % item["description"])

    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
    output.append(process.communicate()[0])
    # output.append(command)
    returncodes.append(process.returncode)

  if 1 in returncodes:
    for item in output:
      response += str(item) + '\n'
    return HttpResponse(response, mimetype='text/plain', status=400)
  else:
    return HttpResponse("ok", mimetype='text/plain')

def list_objects(request, uuid):
  response = []
  job = Job.objects.get(jobuuid=uuid)

  for root, dirs, files in os.walk(job.directory + '/objects', False):
    for name in files:
     directory = root.replace(job.directory + '/objects', '')
     response.append(os.path.join(directory, name))

  return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def explore(request, uuid):
  # Database query
  job = Job.objects.get(jobuuid=uuid)
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
      newItem['size'] = os.path.getsize(os.path.join(directory, item))
    contents.append(newItem)
  return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def ingest(request, uuid=None):
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

def archival_storage(request, path=None):
  document = '/var/archivematica/sharedDirectory/www/index.html'
  # User requests a file, send it (mimetype application/zip)
  if None != path:
    path = os.path.join(os.path.dirname(document), path)
    if os.path.exists(path):
      response = HttpResponse(mimetype='application/zip')
      response['Content-Disposition'] = 'attachment; filename=%s' %  os.path.basename(path)
      with open(path) as resource:
        response.write(resource.read())
      return response
  # Browse contents parsing index.html static file, generated by storeAIP.py
  try:
    tree = etree.parse(document)
  except IOError:
    return render_to_response('main/archival_storage.html', locals())
  tree = tree.findall('body/div')
  sips = []
  for item in tree:
    sip = {}
    sip['href'] = item.find('p[@class="name"]/a').attrib['href']
    sip['name'] = item.find('p[@class="name"]/a').text
    sip['uuid'] = item.find('p[@class="uuid"]').text
    sip['size'] = '{0:.3g}'.format(os.path.getsize(os.path.join(os.path.dirname(document), sip['href'])) / float(1024) / float(1024))
    try:
      date = datetime.strptime(item.find('p[@class="date"]').text.split('.')[0], '%Y-%m-%dT%H:%M:%S')
      sip['date'] = date.isoformat(' ')
    except:
      pass
    sips.append(sip)
    order_by = request.GET.get('order_by', 'name');
    sort_by = request.GET.get('sort_by', 'up');
    def sort_aips(sip):
      value = 0
      if 'name' == order_by:
        value = sip['name'].lower()
      else:
        value = sip[order_by]
      return value
    sips = sorted(sips, key = sort_aips)
    if sort_by == 'down':
      sips.reverse()
  return render_to_response('main/archival_storage.html', locals())

def preservation_planning(request):
  query="""SELECT
      Groups.description,
      FIBE.Extension,
      CC.classification,
      CT.TYPE,
      CR.countAttempts,
      CR.countOK,
      CR.countNotOK,
      CR.countAttempts - (CR.countOK + CR.countNotOK) AS countIncomplete,
      Commands.PK AS CommandPK,
      Commands.description,
      Commands.command
    FROM FileIDsByExtension AS FIBE
    RIGHT OUTER JOIN FileIDs ON FIBE.FileIDs = FileIDs.pk
    LEFT OUTER JOIN FileIDGroupMembers AS FIGM ON FIGM.fileID = FileIDs.pk
    LEFT OUTER JOIN Groups on Groups.pk = FIGM.groupID
    JOIN CommandRelationships AS CR ON FileIDs.pk = CR.FileID
    JOIN Commands ON CR.command = Commands.pk
    JOIN CommandClassifications AS CC on CR.commandClassification = CC.pk
    JOIN CommandTypes AS CT ON Commands.commandType = CT.pk
    WHERE
      FIBE.Extension IS NOT NULL
      AND CC.classification IN ('access', 'preservation')
    ORDER BY Groups.description, FIBE.Extension, CC.classification"""

  cursor = connection.cursor()
  cursor.execute(query)
  planning = cursor.fetchall()

  url = {
    'Audio': 'http://archivematica.org/wiki/index.php?title=Audio',
    'Email': 'http://archivematica.org/wiki/index.php?title=Email',
    'Office Open XML': 'http://archivematica.org/wiki/index.php?title=Microsoft_Office_Open_XML',
    'Plain text': 'http://archivematica.org/wiki/index.php?title=Plain_text',
    'Portable Document Format': 'http://archivematica.org/wiki/index.php?title=Portable_Document_Format',
    'Presentation': 'http://archivematica.org/wiki/index.php?title=Presentation_files',
    'Raster Image': 'http://archivematica.org/wiki/index.php?title=Raster_images',
    'Raw Camera Image': 'http://archivematica.org/wiki/index.php?title=Raw_camera_files',
    'Spreadsheet': 'http://archivematica.org/wiki/index.php?title=Spreadsheets',
    'Vector Image': 'http://archivematica.org/wiki/index.php?title=Vector_images',
    'Video': 'http://archivematica.org/wiki/index.php?title=Video',
    'Word Processing': 'http://archivematica.org/wiki/index.php?title=Word_processing_files'
  }

  file_types = []
  last_type = ''
  for item in planning:
    if last_type == item[0]:
      row = file_types.pop()
    else:
      row = {}
      row['type'] = last_type = item[0] # File type
      if row['type'] in url:
        row['url'] = url[row['type']]
      row['extensions'] = []
    row['extensions'].append(item) # Extensions
    file_types.append(row)

  cursor.close()

  return render_to_response('main/preservation_planning.html', locals())

def normalization_report(request, uuid):

  query = """
    SELECT

      Tasks.fileUUID AS U,
      Tasks.fileName,

      Tasks.fileUUID IN (
        SELECT Tasks.fileUUID
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exitCode = 0 AND
          Tasks.exec = 'transcoderNormalizePreservation_v0.0' AND
          Tasks.stdOut LIKE '%%[Command]%%')
      AS 'Preservation normalization attempted',

      (
        SELECT Tasks.exitCode
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exec = 'transcoderNormalizePreservation_v0.0' AND
          Tasks.fileUUID = U
      ) != 0
      AS 'Preservation normalization failed',


      Tasks.fileUUID IN (
        SELECT Tasks.fileUUID
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exitCode = 0 AND
          Tasks.exec = 'transcoderNormalizePreservation_v0.0' AND
          Tasks.stdOut LIKE '%%Already in preservation format%%')
      AS 'Already in preservation format',

      Tasks.fileUUID NOT IN (
        SELECT Tasks.fileUUID
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exitCode = 0 AND
          Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
          Tasks.stdOut LIKE '%%description: Copying File.%%') AND
          Tasks.fileUUID IN (
            SELECT Tasks.fileUUID
            FROM Tasks
            JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
            WHERE
              Jobs.SIPUUID = %s AND
              Tasks.exitCode = 0 AND
              Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
              Tasks.stdOut LIKE '%%[Command]%%') AND
          Tasks.fileUUID NOT IN (
            SELECT Tasks.fileUUID
            FROM Tasks
              JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
            WHERE
              Jobs.SIPUUID = %s AND
              Tasks.exitCode = 0 AND
              Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
              Tasks.stdOut LIKE '%%Not including %% in DIP.%%')
      AS 'Access normalization attempted',

      (
        SELECT Tasks.exitCode
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
          Tasks.fileUUID = U
      ) != 0
      AS 'Access normalization failed',

      Tasks.fileUUID IN (
        SELECT Tasks.fileUUID
        FROM Tasks
        JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
        WHERE
          Jobs.SIPUUID = %s AND
          Tasks.exitCode = 0 AND
          Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
          Tasks.stdOut LIKE '%%Already in access format%%')
      AS 'Already in access format'

    FROM Tasks
    JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
    WHERE
      Tasks.exec = 'transcoderNormalizePreservation_v0.0' AND
      Jobs.SIPUUID = %s
    ORDER BY Tasks.fileName"""

  cursor = connection.cursor()
  cursor.execute(query, (
    uuid, uuid, uuid, uuid, uuid, uuid, uuid, uuid, uuid
  ))
  objects = cursor.fetchall()

  return render_to_response('main/normalization_report.html', locals())

def tasks(request, uuid):
  job = Job.objects.get(jobuuid=uuid)
  objects = job.task_set.all().order_by('-exitcode', '-endtime', '-starttime', '-createdtime')
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
