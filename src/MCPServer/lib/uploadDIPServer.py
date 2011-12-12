#!/usr/bin/python -OO

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

# @package Archivematica
# @subpackage MCPServer
# @version svn: $Id$

import os
import sys
import gearman
import cPickle
from socket import gethostname
import subprocess
import re
import tempfile
import time

sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
import requests

sys.path.append("/usr/share/archivematica")
os.environ['DJANGO_SETTINGS_MODULE'] = "dashboard.settings"
import dashboard.main.models as models

def start():
    try:
        import archivematicaMCP
        gm_opts = [archivematicaMCP.config.get('MCPServer', 'GearmanServerWorker')]
    except:
        gm_opts = ['127.0.0.1', '4730']
    gm_worker = gearman.GearmanWorker(gm_opts)
    gm_worker.set_client_id(gethostname() + "_MCPServer")

    # Register tasks
    gm_worker.register_task("uploadDIP", uploadDIP)

    if debug():
        print "uploadDIP worker has started, waiting for jobs."

    # Loop
    gm_worker.work()

def uploadDIP(worker, job):

    try:

        if debug():
            print "[uploadDIP] Processing job..."

        # Capture data sent within the job
        data = cPickle.loads(job.data)

        # Got enough information, storage it (we'll update it later)
        access = models.Access()
        access.sipuuid = data.UUID
        access.save()

        # Rsync
        if data.rsync_command and data.rsync_target:

            # Get uploadDIP directory from the database
            jobs = models.Job.objects.filter(sipuuid=data.UUID)
            if jobs.count:
                dir_source = jobs[0].directory

                # Build command
                command = ['rsync', '-avzP', dir_source, dir_target]

                # Getting around of rsync output buffering by outputting to a temporary file
                pipe_output, file_name = tempfile.mkstemp()

                process = subprocess.Popen(command, stdout=pipe_output)

                # poll() returns None while the process is still running
                while not process.poll():
                    time.sleep(1)
                    last_line = open(file_name).readlines()

                    # It's possible that it hasn't output yet, so continue
                    if len(last_line) == 0:
                        continue
                    last_line = last_line[-1]

                    # Matching to "[bytes downloaded]  number%  [speed] number:number:number"
                    match = re.match(".* ([0-9]*)%.* ([0-9]*:[0-9]*:[0-9]*).*", last_line)

                    if not match:
                        continue

                    # Update job status somewhere (MCP.Accesses?)
                    # percentage in match.group(1)
                    # ETA in match.group(2)

                # We don't need the temporary file anymore!
                os.unlink(file_name)

        # Building headers dictionary for the deposit request
        headers = {}
        headers['User-Agent'] = 'Archivematica'
        headers['X-Packaging'] = 'http://purl.org/net/sword-types/METSArchivematicaDIP'
        """ headers['X-On-Beahalf-Of'] """
        headers['Content-Type'] = 'application/zip'
        headers['X-No-Op'] = 'false'
        headers['X-Verbose'] = 'false'
        headers['Content-Location'] = 'file:///A60'
        """ headers['Content-Disposition'] """

        # Auth and request!
        auth = requests.auth.HTTPBasicAuth(data.email, data.password)
        response = requests.request('POST', data.url, auth=auth, headers=headers)

        if debug():
          print "> Response code: %s" % response.status_code
          # print response.content
          # print response.headers
          print "> Location: %s" % response.headers.get('Location')

        # Update record with location
        access.resource = response.headers.get('Location')
        access.save()

    except Exception as inst:
        print >>sys.stderr, "DEBUG EXCEPTION! uploadDIP worker"
        print >>sys.stderr, type(inst)
        print >>sys.stderr, inst.args
        import traceback
        traceback.print_exc(file=sys.stdout)
        return ""

    finally:
        if debug():
            print "[uploadDIP] Job finished"

    return ""

def debug():
    return True
    # return __name__ == "__main__"

if __name__ == "__main__":
    start()
