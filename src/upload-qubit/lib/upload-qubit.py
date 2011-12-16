#!/usr/bin/python -OO
# -*- coding: utf-8 -*-

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
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

import getpass
import optparse
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.append("/usr/lib/archivematica/archivematicaCommon/externals")
import requests

sys.path.append("/usr/share/archivematica")
os.environ['DJANGO_SETTINGS_MODULE'] = "dashboard.settings"
import dashboard.main.models as models

user = getpass.getuser()
if "archivematica" != user:
  print >> sys.stderr, 'This user is required to be executed as "archivematica" user but you are using %s.' % user
  sys.exit(1)

def start(data):

    try:
        # Make sure UUID exists
        if not models.Job.objects.filter(sipuuid=data.UUID).count():
            log("UUID not recognized")
            return ''

        # Get directory
        jobs = models.Job.objects.filter(sipuuid=data.UUID, jobtype="uploadDIP")
        if jobs.count():
            directory = jobs[0].directory.rstrip('/').replace('%sharedPath%', '/var/archivematica/sharedDirectory/')
        else:
            log("Directory not found")
            return ''

        # Nth try
        try:
            access = models.Access.objects.get(sipuuid=data.UUID)
        # First time this job is called
        except:
            access = models.Access()
            access.sipuuid = data.UUID
            access.save()

        # Rsync (data.rsync_target and data.rsync_command (optional))
        if data.rsync_target:
            """ Build command (rsync)
             -a =
                -r = recursive
                -l = recreate symlinks on destination
                -p = set same permissions
                -t = transfer modification times
                -g = set same group owner on destination
                -o = set same user owner on destination (if possible, super-user)
                --devices = transfer character and block device files (only super-user)
                --specials = transfer special files like sockets and fifos
             -z = compress
             -P = --partial + --stats
            """
            command = ["rsync", "-rltz", "-P", directory, data.rsync_target]
            if data.rsync_command:
                # i.e.: rsync -e "ssh -i key"
                command.insert(1, "-e \"%s\"" % data.rsync_command)

            log(' '.join(command))

            # Getting around of rsync output buffering by outputting to a temporary file
            pipe_output, file_name = tempfile.mkstemp()
            log("Rsync output is being saved in %s" % file_name)

            process = subprocess.Popen(command, stdout=pipe_output, stderr=pipe_output)

            # poll() returns None while the process is still running
            while process.poll() is None:
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

                # Update upload status
                # - percentage in match.group(1)
                # - ETA in match.group(2)
                access.status = "Sending... %s (ETA: %s)" % (match.group(1), match.group(2))
                access.save()
                log(access.status)

            # We don't need the temporary file anymore!
            # log("Removing temporary rsync output file: %s" % file_name)
            # os.unlink(file_name)

            # At this point, we should have a return code
            # If greater than zero, see man rsync (EXIT VALUES)
            access.exitcode = process.returncode

            if 0 < process.returncode:
              log("rsync quit unexpectedly (exit %s), the upload script will be stopped here" % process.returncode)
              return ''

            access.save()

        # Building headers dictionary for the deposit request
        headers = {}
        headers['User-Agent'] = 'Archivematica'
        headers['X-Packaging'] = 'http://purl.org/net/sword-types/METSArchivematicaDIP'
        """ headers['X-On-Beahalf-Of'] """
        headers['Content-Type'] = 'application/zip'
        headers['X-No-Op'] = 'false'
        headers['X-Verbose'] = 'false'
        headers['Content-Location'] = "file:///%s" % os.path.basename(directory)
        """ headers['Content-Disposition'] """

        # Auth and request!
        log("About to deposit to: %s" % data.url)
        auth = requests.auth.HTTPBasicAuth(data.email, data.password)
        response = requests.request('POST', data.url, auth=auth, headers=headers)

        # response.{content,headers,status_code}
        log("> Response code: %s" % response.status_code)
        log("> Location: %s" % response.headers.get('Location'))

        # Update record with location
        access.resource = response.headers.get('Location')
        access.save()

    except Exception as inst:
        log("DEBUG EXCEPTION! uploadDIP worker")
        print >>sys.stderr, "DEBUG EXCEPTION! uploadDIP worker"
        print >>sys.stderr, type(inst)
        print >>sys.stderr, inst.args
        import traceback
        traceback.print_exc()
        return ""

    finally:
        log("Upload finished")

    return ""

def log(message):
    if True:
        print "[uploadDIP] %s" % message

if __name__ == '__main__':

    parser = optparse.OptionParser(usage='Usage: %prog [options]')

    options = optparse.OptionGroup(parser, 'Basic options')
    options.add_option('-u', '--url', dest='url', metavar='URL', help='URL')
    options.add_option('-e', '--email', dest='email', metavar='EMAIL', help='account e-mail')
    options.add_option('-p', '--password', dest='password', metavar='PASSWORD', help='account password')
    options.add_option('-U', '--UUID', dest='UUID', metavar='UUID', help='UUID')
    parser.add_option_group(options)

    options = optparse.OptionGroup(parser, 'Rsync options')
    options.add_option('-c', '--rsync-command', dest='rsync_command', metavar='RSYNC_COMMAND', help='Rsync command, e.g.: ssh -p 2222')
    options.add_option('-t', '--rsync-target', dest='rsync_target', metavar='RSYNC_TARGET', help='Rsync target, e.g.: foo@bar:~/dips/')
    parser.add_option_group(options)

    (opts, args) = parser.parse_args()

    if opts.email is None or opts.password is None or opts.url is None or opts.UUID is None:
         print >>sys.stderr, "Invalid syntax"
         parser.print_help()
         sys.exit(2)

    start(opts)

