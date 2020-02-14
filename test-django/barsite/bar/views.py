from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import logout
from bar.models import Cocktail, Persona, Cliente, Barista, ClienteOrdinaCocktailRicevendoCodicePrenotazione, CodicePrenotazione, BaristaGestisceCocktail
from random import randint
import datetime


ordine = []
totale = 0


# GO TO
def goToRegistrazione(request):
    return render(request, 'bar/registrazione.html', None)


def goToHomepage(request):
    return render(request, 'bar/homepage.html', None)


def goToModificaMenu(request, barista_id):
    list_cocktails = Cocktail.objects.all()

    context = {
        'list_cocktails': list_cocktails,
        'barista_id': barista_id,
    }

    return render(request, 'bar/modifica-menu.html', context)


def goToInserisciCocktail(request, barista_id):
    return render(request, 'bar/inserisci-cocktail.html', {'barista_id': barista_id})


def goToModificaCocktail(request, barista_id, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)

    context = {
        'cocktail': c,
        'barista_id': barista_id,
    }
    return render(request, 'bar/modifica-cocktail.html', context)


def goToOrdinazione(request, cliente_id):
    c = Cliente.objects.get(id=cliente_id)

    list_cocktails = Cocktail.objects.all()

    global ordine
    global totale

    context = {
        'list_cocktails': list_cocktails,
        'cliente': c,
        'cliente_id': cliente_id,
        'ordine': ordine,
        'totale': totale,
    }
    return render(request, "bar/ordinazione.html", context)


def goToStorico(request, cliente_id):
    global ordine
    ordine = []
    global totale
    totale = 0

    cliente = Cliente.objects.get(id=cliente_id)

    list_ordinazioni = ClienteOrdinaCocktailRicevendoCodicePrenotazione.objects.filter(fk_id_cliente=cliente)

    cocktails = []
    for ordinazione in list_ordinazioni:
        cocktail = Cocktail.objects.get(id=ordinazione.fk_id_cocktail.id)
        cocktails.append({
            'nome': cocktail.nome,
            'data': ordinazione.data,
        })

    context = {
        'cocktails': cocktails,
        'cliente_id': cliente_id,
    }

    return render(request, 'bar/storico.html', context)

def goToCodicePrenotazione(request):
    return render(request, 'bar/codice-prenotazione.html', None)


# METODI QUERY
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
            # print(not_p)
            return HttpResponse('Nessun utente registrato con queste credenziali.')
        else:
            p_id = p.id

            try:
                type_c = Cliente.objects.get(id=p_id)
            except Cliente.DoesNotExist as not_c:
                # print(not_c)
                try:
                    type_b = Barista.objects.get(id=p_id)
                except Barista.DoesNotExist as not_b:
                    # print(not_b)
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


def inserisciCocktail(request, barista_id):
    if request.method == 'POST':
        nomeCocktail = request.POST.get('nome')
        ingredienti = request.POST.get('ingredienti')
        prezzo = request.POST.get('prezzo')

        cocktail = Cocktail(nome=nomeCocktail, ingredienti=ingredienti, prezzo=prezzo)
        cocktail.save()

        barista = Barista.objects.get(id=barista_id)

        barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=cocktail, fk_id_barista=barista, azione='Inserimento')
        barista_gestisce_cocktail.save()

        context = {
            'nome': nomeCocktail,
            'ingredienti': ingredienti,
            'prezzo': prezzo,
            'barista_id': barista_id,
        }

        return render(request, 'bar/inserimento-avvenuto.html', context)


def modificaCocktail(request, barista_id, cocktail_id):
    if request.method == 'POST':
        ingredienti = request.POST.get('ingredienti')
        prezzo = request.POST.get('prezzo')

        barista = Barista.objects.get(id=barista_id)

        c = Cocktail.objects.get(id=cocktail_id)

        if ingredienti and prezzo:
            c.ingredienti = ingredienti
            c.prezzo = prezzo
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            print('aggiorna entrambi')
        elif not prezzo and ingredienti:
            c.ingredienti = ingredienti
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            print('aggiorna ingredienti')
        elif not ingredienti and prezzo:
            c.prezzo = prezzo
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            print('aggiorna prezzo')
        elif not ingredienti and not prezzo:
            print('non aggiornare nulla')

        c = Cocktail.objects.get(id=cocktail_id)
        context = {
            'cocktail': c,
            'barista_id': barista_id,
        }

        return render(request, 'bar/modifica-avvenuta.html', context)


def ordinazioneCocktail(request, cliente_id, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)

    o = {
        'id': c.id,
        'nome': c.nome,
        'prezzo': c.prezzo,
    }

    global ordine
    ordine = ordina(o)

    context = {
        'c': c,
        'cliente_id': cliente_id,
    }
    return render(request, 'bar/ordinazione-cocktail.html', context)


def ordina(o):
    # print('ordina')
    ordine.append(o)

    global totale
    totale = totale + o['prezzo']

    return ordine


def confermaOrdinazione(request, cliente_id):
    # print(cliente_id)

    global ordine
    # print(ordine)

    codice = randint(1000, 9999)
    # print(codice)

    today = datetime.date.today()

    codice_prenotazione = CodicePrenotazione(codice=codice)
    codice_prenotazione.save()

    cliente = Cliente.objects.get(id=cliente_id)

    for o in ordine:
        cocktail = Cocktail.objects.get(id=o['id'])

        ordinazione = ClienteOrdinaCocktailRicevendoCodicePrenotazione(data=today, fk_id_cocktail=cocktail, fk_id_codice_prenotazione=codice_prenotazione, fk_id_cliente=cliente)
        ordinazione.save()

    context = {
        'codice': codice,
        'cliente_id': cliente_id,
    }

    return render(request, 'bar/ordinazione-avvenuta.html', context)


def eliminaCocktail(request, barista_id, cocktail_id):
    c = Cocktail.objects.get(id=cocktail_id)
    nome = c.nome
    c.delete()

    context = {
        'nome': nome,
        'barista_id': barista_id,
    }
    return render(request, 'bar/elimina-cocktail.html', context)


def codicePrenotazione(request, barista_id):
    # print(barista_id)
    # barista = Barista.objects.get(id=barista_id)
    list_codici = CodicePrenotazione.objects.all()

    context = {
        'list_codici': list_codici,
        'barista_id': barista_id,
    }

    return render(request, 'bar/codice-prenotazione.html', context)


def controlloCodice(request):
    return HttpResponse('Pagina di controllo codice prenotazione.')

