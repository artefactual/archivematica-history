from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea

class DublinCoreMetadataForm(forms.Form):

  TEXTAREA_ATTRS = {'rows': '4', 'class': 'span11'}
  INPUT_ATTRS = {'class': 'span11'}

  title = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  creator = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  subject = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  description = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))
  publisher = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  contributor = forms.CharField(required=False, widget=TextInput(attrs=INPUT_ATTRS))
  date = forms.DateField(required=False, help_text='Use ISO 8061 (YYYY-MM-DD)', widget=TextInput(attrs=INPUT_ATTRS))
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

  TEXTAREA_ATTRS = {'rows': '4', 'class': 'span11'}

  arguments = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))
# ...
