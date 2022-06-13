from django import forms
from .models import OpenRefine

class OpenRefineForm(forms.Form):
    model = OpenRefine

