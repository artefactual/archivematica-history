# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Job(models.Model):
  jobuuid = models.CharField(max_length=150, primary_key=True, db_column='jobUUID')
  jobtype = models.CharField(max_length=750, db_column='jobType', blank=True)
  createdtime = models.DateTimeField(db_column='createdTime')
  directory = models.CharField(max_length=750, blank=True)
  sipuuid = models.CharField(max_length=150, db_column='SIPUUID', blank=True)
  currentstep = models.CharField(max_length=150, db_column='currentStep', blank=True)

  class Meta:
    db_table = u'Jobs'

class Task(models.Model):
  taskuuid = models.CharField(max_length=150, primary_key=True, db_column='taskUUID')
  # jobuuid = models.CharField(max_length=150, db_column='jobUUID', blank=True)
  job = models.ForeignKey(Job, db_column='jobuuid', to_field = 'jobuuid')
  createdtime = models.DateTimeField(db_column='createdTime')
  fileuuid = models.CharField(max_length=150, db_column='fileUUID', blank=True)
  filename = models.CharField(max_length=300, db_column='fileName', blank=True)
  exec_field = models.CharField(max_length=150, db_column='exec', blank=True)
  arguments = models.CharField(max_length=3000, blank=True)
  starttime = models.DateTimeField(db_column='startTime')
  client = models.CharField(max_length=150, blank=True)
  endtime = models.DateTimeField(db_column='endTime')
  exitcode = models.IntegerField(null=True, db_column='exitCode', blank=True)
  stdout = models.TextField(db_column='stdOut', blank=True)
  stderror = models.TextField(db_column='stdError', blank=True)

  class Meta:
    db_table = u'Tasks'

class JobStepCompleted(models.Model):
  pk = models.IntegerField(primary_key=True)
  # jobuuid = models.CharField(max_length=150, db_column='jobUUID', blank=True)
  job = models.ForeignKey(Job, db_column='jobuuid', to_field = 'jobuuid')
  completedtime = models.DateTimeField(db_column='completedTime')
  step = models.CharField(max_length=150, blank=True)

  class Meta:
    db_table = u'jobStepCompleted'

