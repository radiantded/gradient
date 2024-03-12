from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wb', views.wb_index, name='wb'),
    path('yandex<str:mode>', views.yandex_index, name='yandex'),
    path('faq_ozon', views.faq_ozon, name='faq_ozon'),
    path('faq_wb', views.faq_wb, name='faq_wb'),
    path('faq_yandex', views.faq_yandex, name='faq_yandex'),
    path('download/<str:file_name>', views.download, name='download')
]
