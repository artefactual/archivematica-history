from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea

class DublinCoreMetadataForm(forms.Form):

  TEXTAREA_ATTRS = {'rows':'4'}

  title = forms.CharField(required=False)
  creator = forms.CharField(required=False)
  subject = forms.CharField(required=False)
  description = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))
  publisher = forms.CharField(required=False)
  contributor = forms.CharField(required=False)
  date = forms.DateField(required=False, help_text='Use ISO 8061 (YYYY-MM-DD)')
  type = forms.CharField(required=False)
  format = forms.CharField(required=False)
  identifier = forms.CharField(required=False)
  source = forms.CharField(required=False)
  isPartOf = forms.CharField(required=False)
  language = forms.CharField(required=False, help_text='Use ISO 3166')
  coverage = forms.CharField(required=False)
  rights = forms.CharField(required=False, widget=Textarea(attrs=TEXTAREA_ATTRS))

  """
  This form is intended to use for a js template system
  But Django forms.py is escaping all the chars
  def set_initial_value(self):
    for name, field in self.fields.items():
      field.initial = '<%= ' + name + ' %>'
  """

class TransferMetadataForm(forms.Form):
  accession_identifier = forms.CharField()
  source_of_acquisition = forms.CharField()
  type_of_transfer = forms.CharField()
  description = forms.CharField()
  notes = forms.CharField()

# ...
