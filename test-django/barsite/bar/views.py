from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import logout
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

            return HttpResponse('Nessun utente registrato con queste credenziali.')
        else:
            p_id = p.id

            try:
                type_c = Cliente.objects.get(id=p_id)
            except Cliente.DoesNotExist as not_c:

                try:
                    type_b = Barista.objects.get(id=p_id)
                except Barista.DoesNotExist as not_b:

                    return HttpResponse('Nessun utente registrato con queste credenziali.')
                    # inserisci view per questa eccezione
                else:
                    # print(type_b)
                    context = {
                        'persona': p,
                        'type': 'barista',
                    }

                    return render(request, 'bar/area-riservata.html', context)
            else:
                # print(type_c)
                context = {
                    'persona': p,
                    'type': 'cliente',
                }

                return render(request, 'bar/area-riservata.html', context)


def logout(request):
    logout(request)
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
        nomeCocktail = request.POST.get('nome')
        ingredienti = request.POST.get('ingredienti')
        prezzo = request.POST.get('prezzo')

        cocktail = Cocktail(nome=nomeCocktail, ingredienti=ingredienti, prezzo=prezzo)
        cocktail.save()

        context = {
            'nome': nomeCocktail,
            'ingredienti': ingredienti,
            'prezzo': prezzo,
        }

        return render(request, 'bar/inserimento-avvenuto.html', context)


def goToModificaCocktail(request, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)
    return render(request, 'bar/modifica-cocktail.html', {'cocktail': c})


def modificaCocktail(request, cocktail_id):
    if request.method == 'POST':
        ingredienti = request.POST.get('ingredienti')
        prezzo = request.POST.get('prezzo')

        c = Cocktail.objects.get(id=cocktail_id)

        if ingredienti and prezzo:
            c.ingredienti = ingredienti
            c.prezzo = prezzo
            c.save()
            print('aggiorna entrambi')
        elif not prezzo and ingredienti:
            c.ingredienti = ingredienti
            c.save()
            print('aggiorna ingredienti')
        elif not ingredienti and prezzo:
            c.prezzo = prezzo
            c.save()
            print('aggiorna prezzo')
        elif not ingredienti and not prezzo:
            print('non aggiornare nulla')

        c = Cocktail.objects.get(id=cocktail_id)
        context = {
            'cocktail': c,
        }

        return render(request, 'bar/modifica-avvenuta.html', context)


def goToEliminaCocktail(request, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)
    return render(request, 'bar/elimina-cocktail.html', {'cocktail': c})

def eliminaCocktail(request, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)
    c.delete()
    return render(request, 'bar/eliminazione-avvenuta.html', {'cocktail': c})


def controlloCodice(request):
    return HttpResponse('Pagina di controllo codice prenotazione.')

def goToOrdinazione(request):
    list_cocktails = Cocktail.objects.all()

    context = {
        'list_cocktails': list_cocktails,
    }
    return render(request, "bar/ordinazione.html", context)

def faiOrdinazione(request):
    return HttpResponse('pagina di ordinazione')
