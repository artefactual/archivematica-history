from xmlrpclib import ServerProxy, Error

class MCPClient:

  def __init__(self, host = 'localhost', port = 8000):
    self.url = 'http://%s:%d' % (host, port)
    self.server = ServerProxy(self.url)

  def approve_job(self):
    pass

  def get_jobs_awaiting_approval(self):
    return self.server.getJobsAwaitingApproval()
