import os
from django.shortcuts import render_to_response

def get_directory_size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

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
