from django.shortcuts import render, HttpResponse
from .forms import CreateWikidataForm
from django.conf import settings
from .models import CreateWikidata
from .finalPrepareStep import createWikidataItems
from pathlib import Path
import glob
import os


# Create your views here.
def createwikidata(request):
    if request.method == "POST":
        form = CreateWikidataForm(request.POST, request.FILES)
        faculties = CreateWikidata()
        respond = ''
        if form.is_valid():
            faculties.tenureOrEmeritus = form.cleaned_data['tenureOrEmeritus']
            faculties.sourceFile = form.cleaned_data['sourceFile']

            faculties.destination = ''
            fileName = str(faculties.sourceFile)
            filePath = settings.MEDIA_ROOT+'/'
            faculties.save()

            try:
                respond = createWikidataItems(faculties.tenureOrEmeritus, sourceFilePath=filePath,
                                                                 fileName=fileName, destination=settings.MEDIA_ROOT+'/')
            except:
                respond = 'FAIL: An error occurred: {}'.format(error)

            if 'FAIL' in respond:
                [f.unlink() for f in Path(settings.MEDIA_ROOT+'/').glob("*") if f.is_file()]

            return render(request, 'createwikidata/createwikidata.html', context={'message': respond})
    else:
        form = CreateWikidataForm

    return render(request, 'createwikidata/createwikidata.html', {'form': form})

def downloadFile(request):
    filepath = settings.MEDIA_ROOT
    file = glob.glob(filepath + "/**_final.csv", recursive=True)
    download = file[0] if len(file) > 0 else ''

    if os.path.exists(download):
        with open(download, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download)
            return response
    else:
        return HttpResponse(status=404)
