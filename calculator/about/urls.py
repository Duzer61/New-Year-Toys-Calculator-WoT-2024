from django.urls import path

from .views import AboutAuthorView, AboutView

app_name = 'about'

urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('author/', AboutAuthorView.as_view(), name='author'),
]
