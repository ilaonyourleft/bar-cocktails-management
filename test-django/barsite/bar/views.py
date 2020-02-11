from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from bar.models import Cocktail, Persona, Cliente, Barista


# Create your views here.


class HomepageView(generic.ListView):
    template_name = 'bar/homepage.html'
    context_object_name = 'cocktail_list'

    def get_queryset(self):
        return Cocktail.objects.all()


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            p = Persona.objects.get(email=email, password=password)
        except Persona.DoesNotExist as not_p:
            print(not_p)
            return HttpResponse('Nessun utente registrato con queste credenziali.')
        else:
            p_id = p.id

            try:
                type_c = Cliente.objects.get(id=p_id)
            except Cliente.DoesNotExist as not_c:
                print(not_c)
                try:
                    type_b = Barista.objects.get(id=p_id)
                except Barista.DoesNotExist as not_b:
                    print(not_b)
                    return HttpResponse('Nessun utente registrato con queste credenziali.')
                    # inserisci view per questa eccezione
                else:
                    print(type_b)
                    context = {
                        'persona': p,
                        'type': 'barista',
                    }

                    return render(request, 'bar/area-riservata.html', context)
            else:
                print(type_c)
                context = {
                    'persona': p,
                    'type': 'cliente',
                }

                return render(request, 'bar/area-riservata.html', context)


def logout(request):
    return render(request, 'bar/homepage.html', None)


def goToRegistrazione(request):
    return render(request, 'bar/registrazione.html', None)


def registrazione(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')

        context = {
            'nome': nome,
            'cognome': cognome,
            'email': email,
            'telefono': telefono,
            'password': password,
        }

        p = Persona(nome=nome, cognome=cognome, email=email, telefono=telefono, password=password)
        p.save()
        c = Cliente(id=p)
        c.save()

        return render(request, 'bar/registrazione-avvenuta.html', context)


def goToHomepage(request):
    return render(request, 'bar/homepage.html', None)


def goToModificaMenu(request):
    list_cocktails = Cocktail.objects.all()

    context = {
        'list_cocktails': list_cocktails,
    }

    return render(request, 'bar/modifica-menu.html', context)


def codicePrenotazione(request):
    return HttpResponse('Pagina di codice prenotazione.')


def goToInserisciCocktail(request):
    return render(request, 'bar/inserisci-cocktail.html', None)


def inserisciCocktail(request):
    if request.method == 'POST':
        print('sei dentro')
        nomeCocktail = request.POST.get('nome')
        ingredienti = request.POST.get('ingredienti')
        prezzo = request.POST.get('prezzo')

        cocktail = Cocktail(nome=nomeCocktail, ingredienti=ingredienti, prezzo=prezzo)
        cocktail.save()
        list_cocktails= Cocktail.objects.all()

        context = {
            'list_cocktails': list_cocktails

        }

        print(context)

        return render(request, 'bar/modifica-menu.html', context)


def controlloCodice(request):
    return HttpResponse('Pagina di controllo codice prenotazione.')
