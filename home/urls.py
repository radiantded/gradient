from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<str:file_name>', views.download, name='download')
]
