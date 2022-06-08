from django import forms
from .models import DataPrep

# Create a data prep input from
class DataPrepForm(forms.Form):
    model = DataPrep

    fieldQnum = forms.CharField(label='Enter Wikidata item ID for Field of Study ')
    departmentQnum = forms.CharField(label='Enter Wikidata item ID for Department ')
    websiteBaseUrl = forms.CharField(label='Enter base URL for faculty website page ')
    allOnePage = forms.BooleanField(label='Are all faculty bio in one page?', required=False)
    file = forms.FileField(label='Select the file for data preparations step ')
