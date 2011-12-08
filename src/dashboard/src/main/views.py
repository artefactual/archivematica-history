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
from django.conf import settings as django_settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection, transaction
from django.forms.models import modelformset_factory, inlineformset_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils import simplejson
from django.utils.functional import wraps
from django.views.static import serve
from dashboard.contrib.mcp.client import MCPClient
from dashboard.contrib import utils
from dashboard.main import forms
from dashboard.main import models
from lxml import etree
import calendar, os, re, subprocess
from datetime import datetime
from django.shortcuts import redirect

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Utils
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

# Try to update context instead of sending new params
def load_jobs(view):
  @wraps(view)
  def inner(request, uuid, *args, **kwargs):
    jobs = models.Job.objects.filter(sipuuid=uuid)
    if 0 == jobs.count:
      raise Http404
    kwargs['jobs'] = jobs
    kwargs['name'] = utils.get_directory_name(jobs[0])
    return view(request, uuid, *args, **kwargs)
  return inner

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Home
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def home(request):
  return render_to_response('home.html', locals())

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Status
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def status(request):
  client = MCPClient()
  xml = etree.XML(client.list())

  sip_count = len(xml.xpath('//choicesAvailableForUnits/choicesAvailableForUnit/unit/type[text()="SIP"]'))
  transfer_count = len(xml.xpath('//choicesAvailableForUnits/choicesAvailableForUnit/unit/type[text()="Transfer"]'))
  dip_count = len(xml.xpath('//choicesAvailableForUnits/choicesAvailableForUnit/unit/type[text()="DIP"]'))

  response = {'sip': sip_count, 'transfer': transfer_count, 'dip': dip_count}

  return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Ingest
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def ingest_grid(request):
  polling_interval = django_settings.POLLING_INTERVAL
  microservices_help = django_settings.MICROSERVICES_HELP
  return render_to_response('main/ingest/grid.html', locals())

def ingest_status(request, uuid=None):
  if request.method == 'GET':
    # Equivalent to: "SELECT SIPUUID, MAX(createdTime) AS latest FROM Jobs GROUP BY SIPUUID
    objects = models.Job.objects.filter(hidden=False).values('sipuuid').annotate(timestamp=Max('createdtime')).exclude(sipuuid__icontains = 'None').filter(unittype__exact = 'unitSIP')
    mcp_available = False
    try:
      client = MCPClient()
      mcp_status = etree.XML(client.list())
      mcp_available = True
    except Exception: pass
    def encoder(obj):
      items = []
      for item in obj:
        jobs = get_jobs_by_sipuuid(item['sipuuid'])
        item['directory'] = utils.get_directory_name(jobs[0])
        item['timestamp'] = calendar.timegm(item['timestamp'].timetuple())
        item['uuid'] = item['sipuuid']
        item['id'] = item['sipuuid']
        del item['sipuuid']
        item['jobs'] = []
        for job in jobs:
          newJob = {}
          item['jobs'].append(newJob)
          newJob['uuid'] = job.jobuuid
          newJob['microservice'] = job.jobtype #map_known_values(job.jobtype)
          newJob['currentstep'] = job.currentstep #map_known_values(job.currentstep)
          newJob['timestamp'] = '%d.%s' % (calendar.timegm(job.createdtime.timetuple()), str(job.createdtimedec).split('.')[-1])
          try: mcp_status
          except NameError: pass
          else:
            xml_unit = mcp_status.xpath('choicesAvailableForUnit[UUID="%s"]' % job.jobuuid)
            if xml_unit:
              xml_unit_choices = xml_unit[0].findall('choices/choice')
              choices = {}
              for choice in xml_unit_choices:
                choices[choice.find("chainAvailable").text] = choice.find("description").text
              newJob['choices'] = choices
        items.append(item)
      return items
    response = {}
    response['objects'] = objects
    response['mcp'] = mcp_available
    return HttpResponse(simplejson.JSONEncoder(default=encoder).encode(response), mimetype='application/json')
  elif request.method == 'DELETE':
    jobs = models.Job.objects.filter(sipuuid=uuid)
    jobs.update(hidden=True)
    """ MCP
    try:
      mcp_client = MCPClient()
      mcp_list = etree.XML(mcp_client.list())
      for uuid in mcp_list.findall('Job/UUID'):
        if 0 < len(jobs.filter(jobuuid=uuid.text)):
          client.execute(uuid.text)
    except Exception: pass
    """
    response = simplejson.JSONEncoder().encode({'removed': True})
    return HttpResponse(response, mimetype='application/json')

def ingest_metadata(request, uuid):
  try:
    dc = models.DublinCore.objects.get_sip_metadata(uuid)
  except ObjectDoesNotExist:
    dc = models.DublinCore(metadataappliestotype=1, metadataappliestoidentifier=uuid)

  fields = ['title', 'creator', 'subject', 'description', 'publisher',
            'contributor', 'date', 'type', 'format', 'identifier',
            'source', 'isPartOf', 'language', 'coverage', 'rights']

  if request.method == 'POST':
    form = forms.DublinCoreMetadataForm(request.POST)
    if form.is_valid():
      for item in fields:
        setattr(dc, item, form.cleaned_data[item])
      dc.save()
  else:
    initial = {}
    for item in fields:
      initial[item] = getattr(dc, item)
    form = forms.DublinCoreMetadataForm(initial=initial)
    jobs = models.Job.objects.filter(sipuuid=uuid)
    name = utils.get_directory_name(jobs[0])

  return render_to_response('main/ingest/metadata.html', locals())

def ingest_detail(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  is_waiting = jobs.filter(currentstep='Awaiting decision').count() > 0
  name = utils.get_directory_name(jobs[0])
  return render_to_response('main/ingest/detail.html', locals())

def ingest_microservices(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  name = utils.get_directory_name(jobs[0])
  return render_to_response('main/ingest/microservices.html', locals())

def ingest_rights_list(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  name = utils.get_directory_name(jobs[0])
  return render_to_response('main/ingest/rights_list.html', locals())

def ingest_rights_edit(request, uuid, id=None):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  name = utils.get_directory_name(jobs[0])

  max_notes = 1

  if id:
    viewRights = models.RightsStatement.objects.get(pk=id)
    form = forms.RightsForm(instance=viewRights)
    # determine how many empty forms should be shown for children
    extra_copyright_notes = max_notes - len(models.RightsStatementCopyrightNote.objects.filter(rightsstatement=viewRights))
    extra_license_notes = max_notes - len(models.RightsStatementLicenseNote.objects.filter(rightsstatement=viewRights))
  else:
    form = forms.RightsForm(request.POST)
    if request.method != 'POST':
      viewRights = models.RightsStatement()
    extra_copyright_notes = max_notes
    extra_license_notes = max_notes

  # create inline formsets for child elements
  CopyrightNoteFormSet = inlineformset_factory(models.RightsStatement, models.RightsStatementCopyrightNote, extra=extra_copyright_notes, can_delete=False)
  LicenseNoteFormSet = inlineformset_factory(models.RightsStatement, models.RightsStatementLicenseNote, extra=extra_license_notes, can_delete=False)

  # handle form creation/saving
  if request.method == 'POST':
    createdRights = form.save()
    copyrightNoteFormset = CopyrightNoteFormSet(request.POST, instance=createdRights)
    copyrightNoteFormset.save() 
    licenseNoteFormset = LicenseNoteFormSet(request.POST, instance=createdRights)
    licenseNoteFormset.save()
    return redirect('/ingest/' + uuid + '/rights/' + str(createdRights.id))
  else:
    copyrightNoteFormset = CopyrightNoteFormSet(instance=viewRights)
    licenseNoteFormset = LicenseNoteFormSet(instance=viewRights)

  return render_to_response('main/ingest/rights_edit.html', locals())

def ingest_delete(request, uuid):
  jobs = Job.objects.filter(sipuuid=uuid)

  """ MCP
  try:
    mcp_client = MCPClient()
    mcp_list = etree.XML(mcp_client.list())
    for uuid in mcp_list.findall('Job/UUID'):
      if 0 < len(jobs.filter(jobuuid=uuid.text)):
        client.execute(uuid.text)
  except Exception: pass
  """

  jobs.update(hidden=True)
  return HttpResponseRedirect(reverse('dashboard.main.views.ingest_grid'))

def ingest_normalization_report(request, uuid):
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
          Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
          Tasks.stdOut LIKE '%%description: Copying File.%%') AND
          Tasks.fileUUID IN (
            SELECT Tasks.fileUUID
            FROM Tasks
            JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
            WHERE
              Jobs.SIPUUID = %s AND
              Tasks.exec = 'transcoderNormalizeAccess_v0.0' AND
              Tasks.stdOut LIKE '%%[Command]%%') AND
          Tasks.fileUUID NOT IN (
            SELECT Tasks.fileUUID
            FROM Tasks
              JOIN Jobs ON Tasks.jobUUID = Jobs.jobUUID
            WHERE
              Jobs.SIPUUID = %s AND
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

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Transfer
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def transfer_grid(request):
  polling_interval = django_settings.POLLING_INTERVAL
  microservices_help = django_settings.MICROSERVICES_HELP
  return render_to_response('main/transfer/grid.html', locals())

def transfer_status(request, uuid=None):
  if request.method == 'GET':
    # Equivalent to: "SELECT SIPUUID, MAX(createdTime) AS latest FROM Jobs GROUP BY SIPUUID
    objects = models.Job.objects.filter(hidden=False, unittype__exact='unitTransfer').values('sipuuid').annotate(timestamp=Max('createdtime')).exclude(sipuuid__icontains = 'None')
    mcp_available = False
    try:
      client = MCPClient()
      mcp_status = etree.XML(client.list())
      mcp_available = True
    except Exception: pass
    def encoder(obj):
      items = []
      for item in obj:
        jobs = get_jobs_by_sipuuid(item['sipuuid'])
        item['directory'] = utils.get_directory_name(jobs[0])
        item['timestamp'] = calendar.timegm(item['timestamp'].timetuple())
        item['uuid'] = item['sipuuid']
        item['id'] = item['sipuuid']
        del item['sipuuid']
        item['jobs'] = []
        for job in jobs:
          newJob = {}
          item['jobs'].append(newJob)
          newJob['uuid'] = job.jobuuid
          newJob['microservice'] = job.jobtype #map_known_values(job.jobtype)
          newJob['currentstep'] = job.currentstep #map_known_values(job.currentstep)
          newJob['timestamp'] = '%d.%s' % (calendar.timegm(job.createdtime.timetuple()), str(job.createdtimedec).split('.')[-1])
          try: mcp_status
          except NameError: pass
          else:
            xml_unit = mcp_status.xpath('choicesAvailableForUnit[UUID="%s"]' % job.jobuuid)
            if xml_unit:
              xml_unit_choices = xml_unit[0].findall('choices/choice')
              choices = {}
              for choice in xml_unit_choices:
                choices[choice.find("chainAvailable").text] = choice.find("description").text
              newJob['choices'] = choices
        items.append(item)
      return items
    response = {}
    response['objects'] = objects
    response['mcp'] = mcp_available
    return HttpResponse(simplejson.JSONEncoder(default=encoder).encode(response), mimetype='application/json')
  elif request.method == 'DELETE':
    jobs = models.Job.objects.filter(sipuuid=uuid)
    try:
      mcp_client = MCPClient()
      mcp_list = etree.XML(mcp_client.list())
      for uuid in mcp_list.findall('Job/UUID'):
        if 0 < len(jobs.filter(jobuuid=uuid.text)):
          client.execute(uuid.text)
    except Exception: pass
    jobs.update(hidden=True)
    response = simplejson.JSONEncoder().encode({'removed': True})
    return HttpResponse(response, mimetype='application/json')

def transfer_detail(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  name = utils.get_directory_name(jobs[0])
  return render_to_response('main/transfer/detail.html', locals())

def transfer_microservices(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)
  name = utils.get_directory_name(jobs[0])
  return render_to_response('main/transfer/microservices.html', locals())

@load_jobs # Adds jobs, name
def transfer_rights_list(request, uuid, jobs, name):
  rights = models.RightsStatementLinkingAgentIdentifier.objects.all()
  return render_to_response('main/transfer/rights_list.html', locals())

@load_jobs # Adds jobs, name
def transfer_rights_add(request, uuid, jobs, name):

  # Copyright note formset
  CopyrightNoteFormSet = inlineformset_factory(models.RightsStatement, models.RightsStatementCopyrightNote,
                                               form=forms.RightsCopyrightNoteForm, extra=1, max_num=1, can_delete=False)

  # License note formset
  LicenseNoteFormSet = inlineformset_factory(models.RightsStatement, models.RightsStatementLicenseNote,
                                             form=forms.RightsLicenseNoteForm, extra=1, max_num=1, can_delete=False)

  # Rights statement form
  form = forms.RightsForm()

  if request.method == 'POST':
    form = forms.RightsForm(request.POST)
    copyright_note_formset = CopyrightNoteFormSet(request.POST, request.FILES)
    license_note_formset = LicenseNoteFormSet(request.POST, request.FILES)
    if form.is_valid() and copyright_note_formset.is_valid() and license_note_formset.is_valid():
      fo = form.save()
      cn = copyright_note_formset.save(commit=False)
      cn.fkRightsStatement = fo.id
      cn.save()
      ln = license_note_formset.save(commit=False)
      ln.fkRightsStatement = fo.id
      ln.save()
      return HttpResponseRedirect(reverse('dashboard.main.views.transfer_rights_list', args=[uuid]))
  else:
    copyright_note_formset = CopyrightNoteFormSet()
    license_note_formset = LicenseNoteFormSet()
    form = forms.RightsForm()

  return render_to_response('main/transfer/rights_edit.html', locals())

@load_jobs # Adds jobs, name
def transfer_rights_edit(request, uuid, jobs, name, id):
  try:
    right = models.RightsStatementLinkingAgentIdentifier.objects.get(id=id)
  except ObjectDoesNotExist:
    raise Http404

  form = forms.RightsForm(request.POST or None, instance=right)
  if form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('dashboard.main.views.transfer_rights_list', args=[uuid]))

  return render_to_response('main/transfer/rights_edit.html', locals())

@load_jobs # Adds jobs, name
def transfer_rights_delete(request, uuid, jobs, name, id):
  return HttpResponse()

def transfer_delete(request, uuid):
  jobs = models.Job.objects.filter(sipuuid=uuid)

  """ MCP
  try:
    mcp_client = MCPClient()
    mcp_list = etree.XML(mcp_client.list())
    for uuid in mcp_list.findall('Job/UUID'):
      if 0 < len(jobs.filter(jobuuid=uuid.text)):
        client.execute(uuid.text)
  except Exception: pass
  """

  jobs.update(hidden=True)
  return HttpResponseRedirect(reverse('dashboard.main.views.ingest_grid'))

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Archival storage
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def archival_storage(request, path=None):
  document = '/var/archivematica/sharedDirectory/www/index.html'
  # User requests a file
  if path is not None:
    return serve(request, path, document_root=os.path.dirname(document))
  total_size = 0
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
    size = os.path.getsize(os.path.join(os.path.dirname(document), sip['href'])) / float(1024) / float(1024)
    total_size = total_size + size
    sip['size'] = '{0:.2f}'.format(size)
    try:
      date = datetime.strptime(item.find('p[@class="date"]').text.split('.')[0], '%Y-%m-%dT%H:%M:%S')
      sip['date'] = date.isoformat(' ')
    except:
      sip['date'] = ''
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
  total_size = '{0:.2f}'.format(total_size)
  return render_to_response('main/archival_storage.html', locals())

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Preservation planning
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

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
      AND FIBE.Extension NOT IN ('mboxi', 'pst')
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

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Access
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def access_list(request):
  access = models.Access.objects.all()
  return render_to_response('main/access.html', locals())

def access_delete(request, id):
  access = get_object_or_404(models.Access, pk=id)
  access.delete()
  return HttpResponseRedirect(reverse('dashboard.main.views.access_list'))

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Settings
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def settings_list(request):
  settings = models.StandardTaskConfig.objects.all()
  return render_to_response('main/settings/list.html', locals())

def settings_edit(request, id):
  try:
    setting = models.StandardTaskConfig.objects.get(id=id)
  except ObjectDoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = forms.SettingsForm(request.POST)
    if form.is_valid():
      setting.arguments = form.cleaned_data['arguments']
      setting.save()
      return HttpResponseRedirect(reverse('dashboard.main.views.settings_list'))
  else:
    form = forms.SettingsForm(initial={'arguments': setting.arguments})

  return render_to_response('main/settings/edit.html', locals())

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Misc
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def tasks(request, uuid):
  job = models.Job.objects.get(jobuuid=uuid)
  objects = job.task_set.all().order_by('-exitcode', '-endtime', '-starttime', '-createdtime')
  return render_to_response('main/tasks.html', locals())

def map_known_values(value):
  #changes should be made in the database, not this map
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
  jobs = models.Job.objects.filter(sipuuid=uuid).order_by('-createdtime')
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

def jobs_manual_normalization(request, uuid):
  job = models.Job.objects.get(jobuuid=uuid)

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

def jobs_list_objects(request, uuid):
  response = []
  job = models.Job.objects.get(jobuuid=uuid)

  for root, dirs, files in os.walk(job.directory + '/objects', False):
    for name in files:
     directory = root.replace(job.directory + '/objects', '')
     response.append(os.path.join(directory, name))

  return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def jobs_explore(request, uuid):
  # Database query
  job = models.Job.objects.get(jobuuid=uuid)
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
