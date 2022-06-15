from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('options', views.options, name='options'),
]
