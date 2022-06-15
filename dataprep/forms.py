from django import forms
from .models import DataPrep

# Create a data prep input from
class DataPrepForm(forms.Form):
    model = DataPrep
    collegeQnum = forms.CharField(label='Enter College item ID ',
                                  widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    fieldQnum = forms.CharField(label='Enter Wikidata item ID for Field of Study ',
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    departmentQnum = forms.CharField(label='Enter Wikidata item ID for Department ',
                                     widget=forms.TextInput(attrs={'class':'form-control'}))
    websiteBaseUrl = forms.CharField(label='Enter base URL for faculty website page ',
                                     widget=forms.TextInput(attrs={'class':'form-control'}))
    allOnePage = forms.BooleanField(label='Are all faculty bio on one page?', required=False,
                                    widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    file = forms.FileField(label='Select the file for data preparation step ',
                           widget=forms.FileInput(attrs={'class':'form-control'}))

