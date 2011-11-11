def get_directory_name(job):
  """
    Expected format:
    %sharedPath%watchedDirectories/workFlowDecisions/createDip/ImagesSIP-69826e50-87a2-4370-b7bd-406fc8aad94f/
  """
  import re

  directory = job.directory
  uuid = job.sipuuid

  try:
    return re.search(r'^.*/(?P<directory>.*)-[\w]{8}(-[\w]{4}){3}-[\w]{12}[/]{0,1}$', directory).group('directory')
  except:
    pass

  try:
    return re.search(r'^.*/(?P<directory>.*)/$', directory).group('directory')
  except:
    pass

  if directory:
    return directory
  else:
    return uuid
