from django.shortcuts import render
from pathlib import Path
from django.conf import settings

# Create your views here.
def index(request):
    [f.unlink() for f in Path(settings.MEDIA_ROOT + '/').glob("*") if f.is_file()]
    print("Media folder cleaned.")
    return render(request, 'index.html', {})

def options(request):
    return render(request, 'options.html', {})