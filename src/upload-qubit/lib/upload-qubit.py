#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# This script is suppossed to be called by the MCP server

import optparse
import sys
import cPickle
import traceback
import gearman

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s created! Result: %s." % (job_request.job.unique, job_request.state)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

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

    # Serialize the opts object, we're sending it as workload
    data = cPickle.dumps(opts)

    try:
        import archivematicaMCP
        gm_opts = [archivematicaMCP.config.get('MCPServer', 'GearmanServerWorker')]
    except:
        gm_opts = ['127.0.0.1', '4730']

    try:
        gm_client = gearman.GearmanClient(gm_opts)
        job = gm_client.submit_job('uploadDIP', data, background=True, wait_until_complete=False)
        check_request_status(job)
    except:
        print >>sys.stderr, "Something wrong happend, see the traceback:"
        traceback.print_exc(file=sys.stderr)
