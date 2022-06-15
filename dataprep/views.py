from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import DataPrepForm
from django.conf import settings
from .models import DataPrep
from .dataPrepScript import runDataPrepForForm
from pathlib import Path
import glob
import os


# Create your views here.
def dataprep(request):
    if request.method == "POST":
        form = DataPrepForm(request.POST, request.FILES)
        faculties = DataPrep()

        if form.is_valid():
            faculties.collegeQnum = form.cleaned_data['collegeQnum']
            faculties.fieldQnum = form.cleaned_data['fieldQnum']
            faculties.departmentQnum = form.cleaned_data['departmentQnum']
            faculties.websiteBaseUrl = form.cleaned_data['websiteBaseUrl']
            faculties.allOnePage = form.cleaned_data['allOnePage']
            faculties.file = form.cleaned_data['file']
            faculties.save()

            try:
                respond = runDataPrepForForm(settings.MEDIA_ROOT+'/', str(faculties.file), faculties.collegeQnum, faculties.fieldQnum,
                                         faculties.departmentQnum, faculties.websiteBaseUrl,
                                         faculties.allOnePage)
            except BaseException as error:
                respond = 'FAIL: An error occurred: {}'.format(error)

            if 'FAIL' in respond:
                [f.unlink() for f in Path(settings.MEDIA_ROOT + '/').glob("*") if f.is_file()]

            return render(request, 'dataprep/dataPrepForm.html', context={'message': respond})
    else:
        form = DataPrepForm

    return render(request, 'dataprep/dataPrepForm.html', {'form': form})

def downloadReady4or(request):
    filepath = settings.MEDIA_ROOT
    file = glob.glob(filepath + "/**_ready4or.csv", recursive=True)
    download = file[0] if len(file) > 0 else ''

    if os.path.exists(download):
        with open(download, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download)
            return response
    else:
        return HttpResponse(status=404)