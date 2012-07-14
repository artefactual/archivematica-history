from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.db import connection
from django.utils import simplejson
import os
import shutil
import MySQLdb
import tempfile
from django.core.servers.basehttp import FileWrapper

import sys
import uuid
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
import databaseFunctions
from archivematicaCreateStructuredDirectory import createStructuredDirectory

SHARED_DIRECTORY_ROOT = '/var/archivematica/sharedDirectory'
ORIGINALS_DIR         = SHARED_DIRECTORY_ROOT + '/transferBackups/originals'
STANDARD_TRANSFER_DIR = SHARED_DIRECTORY_ROOT + '/watchedDirectories/activeTransfers/standardTransfer'
COMPLETED_TRANSFERS_DIR = SHARED_DIRECTORY_ROOT + '/watchedDirectories/SIPCreation/completedTransfers'

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
        new_entry = None
        if file != '.svn':
            new_entry = {}
            new_entry['name'] = file
            entry['children'].append(new_entry)

        # if entry is a directory, recurse
        child_path = os.path.join(path, file)
        if new_entry != None and os.path.isdir(child_path) and os.access(child_path, os.R_OK):
            directory_to_dict(child_path, directory, new_entry)

    # return fully traversed data
    return directory

def directory_contents(path, contents=[]):
    for entry in os.listdir(path):
        contents.append(os.path.join(path, entry))
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path) and os.access(entry_path, os.R_OK):
            directory_contents(entry_path, contents)
    return contents

def contents(request):
    path = request.GET.get('path', '/home')
    response = directory_to_dict(path)
    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

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

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

def get_temp_directory(request):
    temp_dir = tempfile.mkdtemp()

    response = {}
    response['tempDir'] = temp_dir

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

def copy_transfer_component(request):
    transfer_name = request.POST.get('name', '')
    path = request.POST.get('path', '')
    destination = request.POST.get('destination', '')

    error = None

    if transfer_name == '':
        error = 'No transfer name provided.'
    else:
        if path == '':
            error = 'No path provided.'
        else:
            transfer_dir = os.path.join(destination, transfer_name)
            paths_copied = 0
            #return HttpResponse(transfer_dir)

            # cycle through each path copying files/dirs inside it to transfer dir
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)
                if os.path.isdir(entry_path):
                    destination_dir = os.path.join(transfer_dir, entry)
                    try:
                        shutil.copytree(
                            entry_path,
                            destination_dir
                        )
                    except:
                        error = 'Error copying from ' + entry_path + ' to ' + destination_dir + '.'
                else:
                    shutil.copy(entry_path, transfer_dir)

                paths_copied = paths_copied + 1

    response = {}

    if error != None:
      response['message'] = error
      response['error']   = True
    else:
      response['message'] = 'Copied ' + str(paths_copied) + ' entries.'

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

def copy_to_originals(request):
    filepath = request.POST.get('filepath', '')
    error = check_filepath_exists('/' + filepath)

    if error == None:
        processingDirectory = '/var/archivematica/sharedDirectory/currentlyProcessing/'
        sipName = os.path.basename(filepath)
        #autoProcessSIPDirectory = ORIGINALS_DIR
        autoProcessSIPDirectory = '/var/archivematica/sharedDirectory/watchedDirectories/SIPCreation/SIPsUnderConstruction/'
        tmpSIPDir = os.path.join(processingDirectory, sipName) + "/"
        destSIPDir =  os.path.join(autoProcessSIPDirectory, sipName) + "/"

        sipUUID = uuid.uuid4().__str__()

        createStructuredDirectory(tmpSIPDir)
        databaseFunctions.createSIP(destSIPDir.replace('/var/archivematica/sharedDirectory/', '%sharedPath%'), sipUUID)

        objectsDirectory = os.path.join('/', filepath, 'objects')

        #move the objects to the SIPDir
        for item in os.listdir(objectsDirectory):
            shutil.move(os.path.join(objectsDirectory, item), os.path.join(tmpSIPDir, "objects", item))

        #moveSIPTo autoProcessSIPDirectory
        shutil.move(tmpSIPDir, destSIPDir)

        """
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
        """

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Copy successful.'

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

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

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )

def copy_from_arrange_to_completed(request):
    return copy_to_originals(request)
    """
    sourcepath  = request.POST.get('filepath', '')

    error = check_filepath_exists('/' + sourcepath)

    if error == None:
        sourcepath = os.path.join('/', sourcepath)
        destination = os.path.join(COMPLETED_TRANSFERS_DIR, os.path.basename(sourcepath))

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

    return HttpResponse(
        simplejson.JSONEncoder().encode(response),
        mimetype='application/json'
    )
    """

def copy_to_arrange(request):
    sourcepath  = request.POST.get('filepath', '')
    destination = request.POST.get('destination', '')

    error = check_filepath_exists('/' + sourcepath)

    if error == None:
        # use lookup path to cleanly find UUID
        lookup_path = '%sharedPath%' + sourcepath[SHARED_DIRECTORY_ROOT.__len__():sourcepath.__len__()] + '/'
        cursor = connection.cursor()
        query = 'SELECT unitUUID FROM transfersAndSIPs WHERE currentLocation=%s LIMIT 1'
        cursor.execute(query, (lookup_path, ))
        possible_uuid_data = cursor.fetchone()

        if possible_uuid_data:
          uuid = possible_uuid_data[0]
          
          # remove UUID from destination directory name
          modified_basename = os.path.basename(sourcepath).replace('-' + uuid, '')
        else:
          modified_basename = os.path.basename(sourcepath)

        # confine destination to subdir of originals
        sourcepath = os.path.join('/', sourcepath)
        destination = os.path.join('/', destination) + '/' + modified_basename
        # do a check making sure destination is a subdir of ARRANGE_DIR
        destination = pad_destination_filepath_if_it_already_exists(destination)

        if os.path.isdir(sourcepath):
            try:
                shutil.copytree(
                    sourcepath,
                    destination
                )
            except:
                error = 'Error copying from ' + sourcepath + ' to ' + destination + '.'

            if error == None:
                # remove any metadata and logs folders
                for path in directory_contents(destination):
                    basename = os.path.basename(path)
                    if basename == 'metadata' or basename == 'logs':
                        if os.path.isdir(path):
                            shutil.rmtree(path)
        else:
            shutil.copy(sourcepath, destination)

    response = {}

    if error != None:
        response['message'] = error
        response['error']   = True
    else:
        response['message'] = 'Copy successful.'

    return HttpResponse(
      simplejson.JSONEncoder().encode(response),
      mimetype='application/json'
    )

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

def download(request):
    return send_file(request, '/' + request.GET.get('filepath', ''))

def send_file(request, filepath):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    filename = os.path.basename(filepath)
    extension = os.path.splitext(filepath)[1].lower()

    wrapper = FileWrapper(file(filepath))
    response = HttpResponse(wrapper)

    # force download for certain filetypes
    extensions_to_download = ['.7z', '.zip']
    try:
        index = extensions_to_download.index(extension)
        response['Content-Type'] = 'application/force-download'
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    except:
        if extension == '.html':
            response['Content-type'] = 'text/html'
        else:
            response['Content-type'] = 'text/plain'

    response['Content-Length'] = os.path.getsize(filepath)
    return response
