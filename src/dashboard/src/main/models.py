# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class DublinCoreManager(models.Manager):

  def get_sip_metadata(self, uuid):
    return DublinCore.objects.get(metadataappliestotype__exact=1, metadataappliestoidentifier__exact=uuid)

class DublinCore(models.Model):
  id = models.IntegerField(primary_key=True, db_column='pk')
  metadataappliestotype = models.IntegerField(db_column='metadataAppliesToType')
  metadataappliestoidentifier = models.CharField(max_length=50, blank=True, db_column='metadataAppliesToidentifier')
  title = models.TextField(db_column='title', blank=True)
  creator = models.TextField(db_column='creator', blank=True)
  subject = models.TextField(db_column='subject', blank=True)
  description = models.TextField(db_column='description', blank=True)
  publisher = models.TextField(db_column='publisher', blank=True)
  contributor = models.TextField(db_column='contributor', blank=True)
  date = models.TextField(db_column='date', blank=True)
  type = models.TextField(db_column='type', blank=True)
  format = models.TextField(db_column='format', blank=True)
  identifier = models.TextField(db_column='identifier', blank=True)
  source = models.TextField(db_column='source', blank=True)
  isPartOf = models.TextField(db_column='isPartOf', blank=True)
  language = models.TextField(db_column='language', blank=True)
  coverage = models.TextField(db_column='coverage', blank=True)
  rights = models.TextField(db_column='rights', blank=True) 

  objects = DublinCoreManager()

  class Meta:
    db_table = u'Dublincore'

class Job(models.Model):
  jobuuid = models.CharField(max_length=150, primary_key=True, db_column='jobUUID')
  jobtype = models.CharField(max_length=750, db_column='jobType', blank=True)
  createdtime = models.DateTimeField(db_column='createdTime')
  createdtimedec = models.DecimalField(null=True, db_column='createdTimeDec', blank=True)
  directory = models.CharField(max_length=750, blank=True)
  sipuuid = models.CharField(max_length=150, db_column='SIPUUID', blank=True)
  unittype = models.CharField(max_length=150, db_column='unitType', blank=True)
  currentstep = models.CharField(max_length=150, db_column='currentStep', blank=True)
  microservicegroup = models.CharField(max_length=150, db_column='microserviceGroup', blank=True)
  hidden = models.BooleanField(default=False, blank=False)

  class Meta:
    db_table = u'Jobs'

class StandardTaskConfig(models.Model):
  id = models.IntegerField(primary_key=True, db_column='pk')
  execute = models.TextField(db_column='execute', blank=True)
  arguments = models.TextField(db_column='arguments', blank=True)

  class Meta:
    db_table = u'StandardTasksConfigs'

class Task(models.Model):
  taskuuid = models.CharField(max_length=50, primary_key=True, db_column='taskUUID')
  # jobuuid = models.CharField(max_length=50, db_column='jobUUID', blank=True)
  job = models.ForeignKey(Job, db_column='jobuuid', to_field = 'jobuuid')
  createdtime = models.DateTimeField(db_column='createdTime')
  fileuuid = models.CharField(max_length=50, db_column='fileUUID', blank=True)
  filename = models.CharField(max_length=100, db_column='fileName', blank=True)
  exec_field = models.CharField(max_length=50, db_column='exec', blank=True)
  arguments = models.CharField(max_length=1000, blank=True)
  starttime = models.DateTimeField(db_column='startTime')
  client = models.CharField(max_length=50, blank=True)
  endtime = models.DateTimeField(db_column='endTime')
  stdout = models.TextField(db_column='stdOut', blank=True)
  stderror = models.TextField(db_column='stdError', blank=True)
  exitcode = models.IntegerField(null=True, db_column='exitCode', blank=True)

  class Meta:
    db_table = u'Tasks'

class JobStepCompleted(models.Model):
  id = models.IntegerField(primary_key=True, db_column='pk')
  # jobuuid = models.CharField(max_length=50, db_column='jobUUID', blank=True)
  job = models.ForeignKey(Job, db_column='jobuuid', to_field = 'jobuuid')
  completedtime = models.DateTimeField(db_column='completedTime')
  step = models.CharField(max_length=50, blank=True)

  class Meta:
    db_table = u'jobStepCompleted'
