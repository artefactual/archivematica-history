from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils import simplejson
import os
import shutil

SHARED_DIRECTORY_ROOT = '/var/archivematica/sharedDirectory'
ORIGINALS_DIR         = SHARED_DIRECTORY_ROOT + '/transferBackups/originals'
STANDARD_TRANSFER_DIR = SHARED_DIRECTORY_ROOT + '/watchedDirectories/activeTransfers/standardTransfer'

def directory_to_dict(path, directory={}, entry=False):
    # if starting traversal, set entry to directory root
    if (entry == False):
        entry = directory
        # remove leading slash
        entry['parent'] = os.path.dirname(path)[1:]

    # set standard entry properties
    entry['name'] = os.path.basename(path)
    entry['children'] = []

    # define entries
    for file in os.listdir(path):
        new_entry = {}
        new_entry['name'] = file
        entry['children'].append(new_entry)

        # if entry is a directory, recurse
        child_path = os.path.join(path, file)
        if os.path.isdir(child_path) and os.access(child_path, os.R_OK):
            directory_to_dict(child_path, directory, new_entry)

    # return fully traversed data
    return directory

def contents(request):
    path = request.GET.get('path', '/home')
    response = directory_to_dict(path)
    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def delete(request):
    filepath = request.POST.get('filepath', '')
    filepath = os.path.join('/', filepath)
    error = check_filepath_exists(filepath)

    if error == None:
        filepath = os.path.join(filepath)
        if os.path.isdir(filepath):
            try:
                shutil.rmtree(filepath)
            except:
                error = 'Error attempting to delete directory.'
        else:
            os.remove(filepath)

    response = {}

    if error != None:
      response['message'] = error
      response['error']   = True
    else:
      response['message'] = 'Delete successful.'

    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def copy_to_originals(request):
    filepath = request.POST.get('filepath', '')
    error = check_filepath_exists('/' + filepath)

    if error == None:
        # confine destination to subdir of originals
        filepath = os.path.join('/', filepath)
        destination = os.path.join(ORIGINALS_DIR, os.path.basename(filepath))
        destination = pad_destination_filepath_if_it_already_exists(destination)
        #error = 'Copying from ' + filepath + ' to ' + destination + '.'
        try:
            shutil.copytree(
                filepath,
                destination
            )
        except:
            error = 'Error copying from ' + filepath + ' to ' + destination + '.'

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Copy successful.'

    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def copy_to_start_transfer(request):
    filepath = request.POST.get('filepath', '')
    error = check_filepath_exists('/' + filepath)

    if error == None:
        # confine destination to subdir of originals
        filepath = os.path.join('/', filepath)
        destination = os.path.join(STANDARD_TRANSFER_DIR, os.path.basename(filepath))
        destination = pad_destination_filepath_if_it_already_exists(destination)
        #error = 'Copying from ' + filepath + ' to ' + destination + '.'
        try:
            shutil.copytree(
                filepath,
                destination
            )
        except:
            error = 'Error copying from ' + filepath + ' to ' + destination + '.'

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Copy successful.'

    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def copy_from_arrange_to_start_transfer(request):
    sourcepath  = request.POST.get('filepath', '')

    error = check_filepath_exists('/' + sourcepath)

    if error == None:
        sourcepath = os.path.join('/', sourcepath)
        destination = os.path.join(STANDARD_TRANSFER_DIR, os.path.basename(sourcepath))

        # do check if directory already exists
        if os.path.exists(destination):
            error = 'A transfer with this directory name has already been started.'
        else:
            try:
                shutil.copytree(
                    sourcepath,
                    destination
                )
            except:
                error = 'Error copying from ' + filepath + ' to ' + destination + '.'

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Transfer started.'

    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def copy_to_arrange(request):
    sourcepath  = request.POST.get('filepath', '')
    destination = request.POST.get('destination', '')

    error = check_filepath_exists('/' + sourcepath)

    if error == None:
        # confine destination to subdir of originals
        sourcepath = os.path.join('/', sourcepath)
        destination = os.path.join('/', destination) + '/' + os.path.basename(sourcepath)
        # do a check making sure destination is a subdir of ARRANGE_DIR
        destination = pad_destination_filepath_if_it_already_exists(destination)
        #error = 'Copying from ' + sourcepath + ' to ' + destination + '.'
        try:
            shutil.copytree(
                sourcepath,
                destination
            )
        except:
            error = 'Error copying from ' + sourcepath + ' to ' + destination + '.'

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Copy successful.'

    return HttpResponse(simplejson.JSONEncoder().encode(response), mimetype='application/json')

def check_filepath_exists(filepath):
    error = None
    if filepath == '':
        error = 'No filepath provided.'

    # check if exists
    if error == None and not os.path.exists(filepath):
        error = 'Filepath ' + filepath + ' does not exist.'

    # check if is file or directory

    # check for trickery
    try:
        filepath.index('..')
        error = 'Illegal path.'
    except:
        pass

    return error

def pad_destination_filepath_if_it_already_exists(filepath, original=None, attempt=0):
    if original == None:
        original = filepath
    attempt = attempt + 1
    if os.path.exists(filepath):
        return pad_destination_filepath_if_it_already_exists(original + '_' + str(attempt), original, attempt)
    return filepath
