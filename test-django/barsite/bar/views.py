from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from django.views import generic
from bar.models import Persona
from bar.models import Cocktail


# def home(request):
#     #return HttpResponse('Hello, world. You are at the home page. Do you want to check the menu?')
#     cocktail_list = Cocktail.objects.all()
#     context = {
#             'cocktail_list': cocktail_list,
#         }
#     return render(request, 'bar/homepage.html', context)

class HomepageView(generic.ListView):
    template_name = 'bar/homepage.html'
    context_object_name = 'cocktail_list'

    def get_queryset(self):
        return Cocktail.objects.all()
