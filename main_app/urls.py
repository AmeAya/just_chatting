from django.urls import path
from .views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('test', TemplateView.as_view(template_name='test.html')),

]
