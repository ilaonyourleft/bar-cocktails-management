from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from django.views import generic
from bar.models import Cocktail, Persona


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


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        p = Persona.objects.get(email=email, password=password)

        print(p)

        context = {
            'persona': p,
        }

        # return HttpResponse(str(email) + ' and ' + str(password))
        return render(request, 'bar/ordinazione.html', context)


def registrazione(request):
    return HttpResponse('Pagina di registrazione.')


def ordinazione(request):
    return HttpResponse('Pagina di ordinazione.')


def codicePrenotazione(request):
    return HttpResponse('Pagina di codice prenotazione.')


def modificaMenu(request):
    return HttpResponse('Pagina di modifica menu.')


def inserisciCocktail(request):
    return HttpResponse('Pagina di inserimento cocktail.')


def controlloCodice(request):
    return HttpResponse('Pagina di controllo codice prenotazione.')
