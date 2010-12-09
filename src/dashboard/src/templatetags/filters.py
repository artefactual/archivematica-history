from django import template
register = template.Library()

@register.filter('sort_jobs')
def sort_jobs(value):

  return sorted(value, key = lambda value: value.currentstep, reverse = True)

@register.filter('has_errors')
def has_errors(value, sipuuid):

  return 0 < value.filter(sipuuid=sipuuid).filter(currentstep='completedUnsuccessfully').count()

@register.filter('get_first_job')
def get_first_job(value, sipuuid):

  return value.filter(sipuuid=sipuuid).order_by('createdtime')[0].createdtime

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
