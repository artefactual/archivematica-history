import os
from django import template

register = template.Library()

@register.filter('join_path')
def join_path(value, path):
  return os.path.join(value, path)

@register.filter('is_file')
def is_file(value, basedir):
  return os.path.isfile(os.path.join(basedir, value))

@register.filter('is_dir')
def is_dir(value, basedir):
  return os.path.isdir(os.path.join(basedir, value))

@register.filter('get_jobs_by_sipuuid')
def get_jobs_by_sipuuid(value):
  from dashboard.main.models import Job
  jobs = Job.objects.all().filter(sipuuid = value).order_by('-createdtime')
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

@register.filter('map_known_values')
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
