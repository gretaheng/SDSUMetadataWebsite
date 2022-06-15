from django import forms
from .models import CreateWikidata

# Create a data prep input from
class CreateWikidataForm(forms.Form):
    model = CreateWikidata
    TYPE_SELECT = [('t', 'Tenure'), ('e', 'Emeritus')]
    tenureOrEmeritus = forms.CharField(label='Choose which type of faculty ',
                                       widget=forms.RadioSelect(choices=TYPE_SELECT, attrs={'class': 'Radio'}))
    sourceFile = forms.FileField(label='Select the file for wikidata item creation ',
                                 widget=forms.FileInput(attrs={'class':'form-control'}))

