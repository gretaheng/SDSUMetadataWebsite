from django import forms
from .models import CreateWikidata

# Create a data prep input from
class CreateWikidataForm(forms.Form):
    model = CreateWikidata

    tenureOrEmeritus = forms.CharField(label='Enter \'t\' for Tenure or \'e\' for Emeritus ')
    sourceFile = forms.FileField(label='Select the file for data preparations step ')

