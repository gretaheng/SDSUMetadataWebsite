from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.createwikidata, name='createwikidata'),
    path('download_final_file/', views.downloadFinalFile, name='downloadFinalFile'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

