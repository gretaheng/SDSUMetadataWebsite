import os, fnmatch
import glob
import time

from django.shortcuts import render, redirect
from .openRefineScript import openRefineSteps, timerprint
from .form import OpenRefineForm
from pathlib import Path
from django.conf import settings


# Create your views here.

def openrefine(request):
    filepath = settings.MEDIA_ROOT
    file = glob.glob(filepath + "/**ready4or.csv", recursive=True)
    ready4or = file[0] if len(file) > 0 else ''
    nextReady = False

    if request.method == "POST":
        form = OpenRefineForm(request.POST)
        print("Ready to Process ", ready4or)

        if ready4or == '':
            nextReady = False
            return render(request, 'openrefine/openrefine.html', {'nextReady': nextReady})
        else:
            try:
                response = openRefineSteps(ready4or)
            except BaseException as error:
                response = 'FAIL: An error occurred: {}'.format(error)

            nextReady = False if 'FAIL' in response else True

            [f.unlink() for f in Path(settings.MEDIA_ROOT + '/').glob("*") if f.is_file()]
            print("All files deleted, after refining.")

            return render(request, 'openrefine/openrefine.html', {'nextReady': nextReady, 'response': response})
    else:
        form = OpenRefineForm

    return render(request, 'openrefine/openrefine.html', {'form': form, 'file': ready4or, 'nextReady': nextReady})
