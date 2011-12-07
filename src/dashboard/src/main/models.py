# This Django model module was auto-generated and then updated manually
# Needs some cleanups, make sure each model has its primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

from dashboard.contrib import utils
import dashboard.main

class Access(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  sipuuid = models.CharField(max_length=150, db_column='SIPUUID', blank=True)
  resource = models.TextField(db_column='resource', blank=True)
  createdtime = models.DateTimeField(db_column='createdTime')

  class Meta:
    db_table = u'Accesses'

  def get_title(self):
    try:
      jobs = dashboard.main.models.Job.objects.filter(sipuuid=self.sipuuid)
      return utils.get_directory_name(jobs[0])
    except:
      return 'N/A'

class DublinCoreManager(models.Manager):

  def get_sip_metadata(self, uuid):
    return DublinCore.objects.get(metadataappliestotype__exact=1, metadataappliestoidentifier__exact=uuid)

class DublinCore(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
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
  id = models.AutoField(primary_key=True, db_column='pk')
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
  id = models.AutoField(primary_key=True, db_column='pk')
  # jobuuid = models.CharField(max_length=50, db_column='jobUUID', blank=True)
  job = models.ForeignKey(Job, db_column='jobuuid', to_field = 'jobuuid')
  completedtime = models.DateTimeField(db_column='completedTime')
  step = models.CharField(max_length=50, blank=True)

  class Meta:
    db_table = u'jobStepCompleted'

class RightsStatement(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  rightsstatementidentifier = models.TextField(db_column='rightsStatementIdentifier', blank=True, verbose_name='Identifier')
  rightsstatementidentifiertype = models.TextField(db_column='rightsStatementIdentifierType', blank=True, verbose_name='Type')
  rightsstatementidentifiervalue = models.TextField(db_column='rightsStatementIdentifierValue', blank=True, verbose_name='Value')
  rightsbasis = models.TextField(db_column='rightsBasis', blank=True)
  #copyrightinformation = models.TextField(db_column='copyrightInformation', blank=True)
  copyrightstatus = models.TextField(db_column='copyrightStatus', blank=True)
  copyrightjurisdiction = models.TextField(db_column='copyrightJurisdiction', blank=True)
  copyrightstatusdeterminationdate = models.TextField(db_column='copyrightStatusDeterminationDate', blank=True)
  licenseinformation = models.TextField(db_column='licenseInformation', blank=True)
  licenseidentifier = models.TextField(db_column='licenseIdentifier', blank=True)
  licenseidentifiertype = models.TextField(db_column='licenseIdentifierType', blank=True)
  licenseidentifiervalue = models.TextField(db_column='licenseIdentifierValue', blank=True)
  licenseterms = models.TextField(db_column='licenseTerms', blank=True)

  class Meta:
    db_table = u'RightsStatement'

class RightsStatementCopyrightNote(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk', editable=False)
  rightsstatement = models.ForeignKey(RightsStatement, db_column='fkRightsStatement')
  copyrightnote = models.TextField(db_column='copyrightNote', blank=True, verbose_name='Note')

  class Meta:
    db_table = u'RightsStatementCopyrightNote'

class RightsStatementLicenseNote(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk', editable=False)
  rightsstatement = models.ForeignKey(RightsStatement, db_column='fkRightsStatement')
  licensenote = models.TextField(db_column='licenseNote', blank=True)

  class Meta:
    db_table = u'RightsStatementLicenseNote'

class RightsStatementLinkingAgentIdentifier(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  rightsstatement = models.ForeignKey(RightsStatement, db_column='fkRightsStatement')
  # rightsstatement = models.ManyToManyField(RightsStatement, db_column='fkRightsStatement')
  linkingagentidentifiertype = models.TextField(db_column='linkingAgentIdentifierType', blank=True)
  linkingagentidentifiervalue = models.TextField(db_column='linkingAgentIdentifierValue', blank=True)

  class Meta:
    db_table = u'RightsStatementLinkingAgentIdentifier'

class RightsStatementLinkingAgentIdentifierLinkingAgentRole(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  linkingagent = models.ForeignKey(RightsStatementLinkingAgentIdentifier, db_column='fkRightsStatementLinkingAgentIdentifier')
  linkingagentrole = models.TextField(db_column='linkingAgentRole', blank=True)

  class Meta:
    db_table = u'RightsStatementLinkingAgentIdentifierLinkingAgentRole'

class RightsStatementRightsGranted(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  rightsstatement = models.ForeignKey(RightsStatement, db_column='fkRightsStatement')

  class Meta:
    db_table = u'RightsStatementRightsGranted'

class RightsStatementRightsGrantedRestriction(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  rightsgranted = models.ForeignKey(RightsStatementRightsGranted, db_column='fkRightsStatementRightsGranted')
  rightsgrantednote = models.TextField(db_column='rightsGrantedNote', blank=True)

  class Meta:
    db_table = u'RightsStatementRightsGrantedRestriction'

class RightsStatementStatuteInformation(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  rightsstatement = models.ForeignKey(RightsStatement, db_column='fkRightsStatement')
  statutejurisdiction = models.TextField(db_column='statuteJurisdiction', blank=True)
  statutecitation = models.TextField(db_column='statuteCitation', blank=True)
  statuteinformationdeterminationdate = models.TextField(db_column='statuteInformationDeterminationDate', blank=True)

  class Meta:
    db_table = u'RightsStatementStatuteInformation'

class RightsStatementStatuteInformationNote(models.Model):
  id = models.AutoField(primary_key=True, db_column='pk')
  statuteinformation = models.ForeignKey(RightsStatementStatuteInformation, db_column='fkRightsStatementStatuteInformation')
  statutenote = models.TextField(db_column='statuteNote', blank=True)

  class Meta:
    db_table = u'RightsStatementStatuteInformationNote'
