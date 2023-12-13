from django.urls import path

from . import views

app_name = 'calc'


urlpatterns = [
    path('', views.index, name='index'),
    path('national/', views.national, name='national'),
    path('christmas/', views.christmas, name='christmas'),
    path('eastern/', views.eastern, name='eastern'),
    path('magic/', views.magic, name='magic'),
]
