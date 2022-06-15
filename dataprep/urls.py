from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dataprep, name='dataprep'),
    path('download_ready4or/', views.downloadReady4or, name='downloadReady4or'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
