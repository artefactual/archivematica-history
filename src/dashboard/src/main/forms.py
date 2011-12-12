from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.widgets import TextInput, Textarea
from dashboard.main import models

TEXTAREA_ATTRS = {'rows': '4', 'class': 'span11'}
INPUT_ATTRS = {'class': 'span11'}

class DublinCoreMetadataForm(forms.Form):
  title = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  creator = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  subject = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  description = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))
  publisher = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  contributor = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  date = forms.DateField(required=False, help_text='Use ISO 8061 (YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD)', widget=TextInput(attrs=INPUT_ATTRS))
  type = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  format = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  identifier = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  source = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  isPartOf = forms.CharField(required=True, label='isPartOf', widget=TextInput(attrs=INPUT_ATTRS))
  language = forms.CharField(required=False, help_text='Use ISO 3166', widget=TextInput(attrs=INPUT_ATTRS))
  coverage = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  rights = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))

class TransferMetadataForm(forms.Form):
  accession_identifier = forms.CharField()
  source_of_acquisition = forms.CharField()
  type_of_transfer = forms.CharField()
  description = forms.CharField()
  notes = forms.CharField()

class SettingsForm(forms.Form):
  arguments = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))

class RightsForm(ModelForm):
  rightsbasis = forms.ChoiceField(choices=(
    ('Copyright', 'Copyright'),
    ('Statute', 'Statute'),
    ('License', 'License'),
    ('Policy', 'Policy'),
    ('Donor', 'Donor')
  ))

  class Meta:
    model = models.RightsStatement

    #fields = (
    #  'rightsstatementidentifier',)
    exclude = ('id', 'rightsstatementidentifier', 'rightsstatementidentifiertype', 'rightsstatementidentifiervalue',)
    widgets = {
      'rightsstatementidentifier': TextInput(attrs=INPUT_ATTRS), 'rightsnotes': Textarea(attrs=TEXTAREA_ATTRS), 'rightsbasis': TextInput(attrs=INPUT_ATTRS), }

class RightsGrantedForm(ModelForm):
  class Meta:
    model = models.RightsStatementRightsGranted

    widgets = {
      'act': TextInput(attrs=INPUT_ATTRS), 'restriction': TextInput(attrs=INPUT_ATTRS), 'startdate': TextInput(attrs=INPUT_ATTRS), 'enddate': TextInput(attrs=INPUT_ATTRS), }

class RightsCopyrightForm(ModelForm):
  class Meta:
    model = models.RightsStatementCopyright
    widgets = {
      'copyrightstatus': TextInput(attrs=INPUT_ATTRS), 'copyrightjurisdiction': TextInput(attrs=INPUT_ATTRS), 'copyrightstatusdeterminationdate': TextInput(attrs=INPUT_ATTRS), }

class RightsCopyrightNoteForm(ModelForm):
  class Meta:
    model = models.RightsStatementCopyrightNote
    widgets = {
      'copyrightnote': Textarea(attrs=TEXTAREA_ATTRS), }

class RightsStatuteForm(ModelForm):
  class Meta:
    model = models.RightsStatementStatuteInformation
    widgets = {
      'statutejurisdiction': TextInput(attrs=INPUT_ATTRS), 'statutecitation': TextInput(attrs=INPUT_ATTRS), 'statutedeterminationdate': TextInput(attrs=INPUT_ATTRS), }

class RightsLicenseForm(ModelForm):
  class Meta:
    model = models.RightsStatementLicense
    widgets = {
      'licenseidentifier': TextInput(attrs=INPUT_ATTRS), 'licenseterms': TextInput(attrs=INPUT_ATTRS), }

class RightsLicenseNoteForm(ModelForm):
  class Meta:
    model = models.RightsStatementLicenseNote
    widgets = {
      'licensenote': Textarea(attrs=TEXTAREA_ATTRS), }

class RightsStatementLinkingAgentIdentifierForm(ModelForm):
  class Meta:
    model = models.RightsStatementLinkingAgentIdentifier
    exclude = ('linkingagentidentifiertype',)
    widgets = {
      'linkingagentidentifiervalue': TextInput(attrs=INPUT_ATTRS), }

#class RightsLinkingAgent(ModelForm):
#  class Meta:
#    model = models.RightsStatementLinkingAgentIdentifier
