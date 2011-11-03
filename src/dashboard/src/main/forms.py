from django import forms

class DublinCoreMetadataForm(forms.Form):
  title = forms.CharField()
  creator = forms.CharField()
  subject = forms.CharField()
  description = forms.CharField()
  publisher = forms.CharField()
  contributor = forms.CharField()
  date = forms.CharField()
  type = forms.CharField()
  format = forms.CharField()
  identifier = forms.CharField()
  source = forms.CharField()
  isPartOf = forms.CharField()
  language = forms.CharField()
  coverage = forms.CharField()
  rights = forms.CharField()

class TransferMetadataForm(forms.Form):
  accession_identifier = forms.CharField()
  source_of_acquisition = forms.CharField()
  type_of_transfer = forms.CharField()
  description = forms.CharField()
  notes = forms.CharField()
