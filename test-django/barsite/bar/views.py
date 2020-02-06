from django.shortcuts import render
from django.http import HttpResponse
from .models import Persona
from django.template import loader


# Create your views here.

def home(request):
    return HttpResponse('Hello, world. You are at the home page. Do you want to check the menu?')

