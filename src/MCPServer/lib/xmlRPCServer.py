#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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

# @package Archivematica
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import archivematicaMCP
import sys
from linkTaskManagerChoice import choicesAvailableForUnits
import lxml.etree as etree
import gearman
import cPickle
from socket import gethostname


def getJobsAwaitingApproval():
    ret = etree.Element("choicesAvailableForUnits")
    for UUID, choice in choicesAvailableForUnits.items():
        ret.append(choice.xmlify())
    return etree.tostring(ret, pretty_print=True)


def approveJob(jobUUID, chain):
    print "approving: ", jobUUID, chain
    if jobUUID in choicesAvailableForUnits:
        choicesAvailableForUnits[jobUUID].proceedWithChoice(chain)
    return "approving: ", jobUUID, chain

def gearmanApproveJob(gearman_worker, gearman_job):
    try:
        #execute = gearman_job.task
        data = cPickle.loads(gearman_job.data)
        jobUUID = data["jobUUID"]
        chain = data["chain"]
        ret = cPickle.dumps(approveJob(jobUUID, chain))
        if not ret:
            ret = ""
        return ""
    #catch OS errors
    except Exception as inst:
        print >>sys.stderr, "DEBUG EXCEPTION! gearmanApproveJob"
        print >>sys.stderr, type(inst)     # the exception instance
        print >>sys.stderr, inst.args
        return ""

def gearmanGetJobsAwaitingApproval(gearman_worker, gearman_job):
    try:
        #print "DEBUG - getting list of jobs"
        #execute = gearman_job.task
        ret = cPickle.dumps(getJobsAwaitingApproval())
        #print ret
        if not ret:
            ret = ""
        return ret
    #catch OS errors
    except Exception as inst:
        print >>sys.stderr, "DEBUG EXCEPTION! gearmanGetJobsAwaitingApproval"
        print >>sys.stderr, type(inst)     # the exception instance
        print >>sys.stderr, inst.args
        return ""


def startXMLRPCServer():
    gm_worker = gearman.GearmanWorker([archivematicaMCP.config.get('MCPServer', 'GearmanServerWorker')])
    hostID = gethostname() + "_MCPServer"
    gm_worker.set_client_id(hostID)
    gm_worker.register_task("approveJob", gearmanApproveJob)
    gm_worker.register_task("getJobsAwaitingApproval", gearmanGetJobsAwaitingApproval)
    gm_worker.work()
