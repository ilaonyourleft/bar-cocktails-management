from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
from django.views import generic
from bar.models import Cocktail, Persona
from .forms import Registrazione


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
    #next = request.GET.get('next')
    if request.method == 'POST':
        form = Registrazione(request.POST)
    if form.is_valid():
        cliente = form.save(commit=False)
        password = form.cleaned_data.get('password')
        cliente.set_password(password)
        cliente.save()
        nuovo_cliente = login(email=cliente.email, password=cliente.password)
        login(request, nuovo_cliente)
        #if next:
            #return redirect(next)
        #return redirect('/')
    return render(request, 'registrazione.html', {'form': form})
    # if request.method == 'POST':
    #     nome = request.POST.get('nome')
    #     cognome = request.POST.get('cognome')
    #     email = request.POST.get('email')
    #     telefono = request.POST.get('telefono')
    #     password = request.POST.get('password')
    #
    # form = Persona.objects.get(nome ='nome', cognome ='cognome', email=email, telefono ='telefono', password=password)
    # #print(form)
    # context = {
    #     'form': form,
    # }
    # return render(request, "bar/registrazione.html", context)
    #return HttpResponse('Pagina di registrazione.')


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
