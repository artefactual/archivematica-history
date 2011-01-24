from django.conf import settings
from xmlrpclib import ServerProxy, Error
import socket

class MCPClient:

  def __init__(self, host = settings.MCP_SERVER[0], port = settings.MCP_SERVER[1]):
    self.url = 'http://%s:%d' % (host, port)
    self.server = ServerProxy(self.url)
    socket.setdefaulttimeout(3)

  def approve_job(self, uuid):
    return self.server.approveJob(uuid)

  def get_jobs_awaiting_approval(self):
    return self.server.getJobsAwaitingApproval()

  def reject_job(self, uuid):
    return self.server.rejectJob(uuid)