from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home(request):
    return HttpResponse('Hello, world. You are at the home page. Do you want to check the menu?')