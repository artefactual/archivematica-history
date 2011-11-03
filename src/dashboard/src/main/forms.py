from django import forms

class DublinCoreMetadataForm(forms.Form):
  title = forms.CharField(required=False)
  creator = forms.CharField(required=False)
  subject = forms.CharField(required=False)
  description = forms.CharField(required=False)
  publisher = forms.CharField(required=False)
  contributor = forms.CharField(required=False)
  date = forms.CharField(required=False)
  type = forms.CharField(required=False)
  format = forms.CharField(required=False)
  identifier = forms.CharField(required=False)
  source = forms.CharField(required=False)
  isPartOf = forms.CharField(required=False)
  language = forms.CharField(required=False)
  coverage = forms.CharField(required=False)
  rights = forms.CharField(required=False)

class TransferMetadataForm(forms.Form):
  accession_identifier = forms.CharField()
  source_of_acquisition = forms.CharField()
  type_of_transfer = forms.CharField()
  description = forms.CharField()
  notes = forms.CharField()
