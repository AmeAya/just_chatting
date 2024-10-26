from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('test', TemplateView.as_view(template_name='test.html')),
    path('login', login_view, name='login_url'),
    path('', main_view, name='main_url'),
]
