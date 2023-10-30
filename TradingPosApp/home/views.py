from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import TemplateView

# Create your views here.
def home(request):
    return HttpResponse('Hello World')