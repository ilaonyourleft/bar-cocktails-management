from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from bar.models import Cocktail, Persona, Cliente, Barista, ClienteOrdinaCocktailRicevendoCodicePrenotazione, CodicePrenotazione, BaristaGestisceCocktail
from random import randint
import datetime
from django.db import connection


ordine = []
totale = 0


# GO TO
def goToRegistrazione(request):
    return render(request, 'bar/registrazione.html', None)


def goToHomepage(request):
    return render(request, 'bar/homepage.html', None)


def goToModificaMenu(request, barista_id):
    # con raw query
    # list_cocktails = Cocktail.objects.raw('select * from main.Cocktail;')

    # senza raw query
    list_cocktails = Cocktail.objects.all()

    context = {
        'list_cocktails': list_cocktails,
        'barista_id': barista_id,
    }

    return render(request, 'bar/modifica-menu.html', context)


def goToInserisciCocktail(request, barista_id):
    return render(request, 'bar/inserisci-cocktail.html', {'barista_id': barista_id})


def goToModificaCocktail(request, barista_id, cocktail_id):
    # con raw query
    # c = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [cocktail_id])
    #
    # context = {
    #     'cocktail': c[0],
    #     'barista_id': barista_id,
    # }

    # senza raw query
    c = Cocktail.objects.get(id=cocktail_id)

    context = {
        'cocktail': c,
        'barista_id': barista_id,
    }

    return render(request, 'bar/modifica-cocktail.html', context)


def goToOrdinazione(request, cliente_id):
    global ordine
    global totale

    # con raw query
    # c = Cliente.objects.raw('select * from main.Cliente where id = %s;', [cliente_id])
    #
    # list_cocktails = Cocktail.objects.raw('select * from main.Cocktail;')
    #
    # context = {
    #     'list_cocktails': list_cocktails,
    #     'cliente': c[0],
    #     'cliente_id': cliente_id,
    #     'ordine': ordine,
    #     'totale': totale,
    # }

    # senza raw query
    c = Cliente.objects.get(id=cliente_id)

    list_cocktails = Cocktail.objects.all()

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

    # con raw query
    # cliente = Cliente.objects.raw('select * from main.Cliente where id = %s;', [cliente_id])
    #
    # list_ordinazioni = ClienteOrdinaCocktailRicevendoCodicePrenotazione.objects.raw('select * from main.Cliente_ordina_cocktail_ricevendo_codice_prenotazione where fk_id_cliente = %s;', [cliente[0].id.id])
    #
    # cocktails = []
    # for ordinazione in list_ordinazioni:
    #     cocktail = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [ordinazione.fk_id_cocktail.id])
    #     cocktails.append({
    #         'nome': cocktail[0].nome,
    #         'data': ordinazione.data,
    #     })

    # senza raw query
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


def goToCodicePrenotazione(request, barista_id):
    # con raw query
    # list_codici = CodicePrenotazione.objects.raw('select * from main.Codice_prenotazione where fk_id_barista is null;')

    # senza raw query
    list_codici = CodicePrenotazione.objects.filter(fk_id_barista=None)

    context = {
        'list_codici': list_codici,
        'barista_id': barista_id,
    }

    return render(request, 'bar/codice-prenotazione.html', context)


# METODI QUERY
class HomepageView(generic.ListView):
    template_name = 'bar/homepage.html'
    context_object_name = 'cocktail_list'

    def get_queryset(self):
        # con raw query
        # return Cocktail.objects.raw('select * from main.Cocktail;')

        # senza raw query
        return Cocktail.objects.all()


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # con raw query
        # try:
        #     p = Persona.objects.raw('select * from main.Persona where email = %s and password = %s;', [email, password])
        # except Persona.DoesNotExist as not_p:
        #     # print(not_p)
        #     return HttpResponse('Nessun utente registrato con queste credenziali.')
        # else:
        #     p_id = p[0].id
        #     type_c = Cliente.objects.raw('select * from main.Cliente where id = %s;', [p_id])
        #     if not type_c:
        #         type_b = Barista.objects.raw('select * from main.Barista where id = %s;', [p_id])
        #         if type_b:
        #             context = {
        #                     'persona': p[0],
        #                     'type': 'barista',
        #                 }
        #     else:
        #         context = {
        #                 'persona': p[0],
        #                 'type': 'cliente',
        #             }
        #     return render(request, 'bar/area-riservata.html', context)

        # senza raw query
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

        # con raw query
        # cursor_p = connection.cursor()
        # cursor_p.execute('insert into main.Persona(nome, cognome, email, telefono, password) values(%s, %s, %s, %s, %s);', [nome, cognome, email, telefono, password])
        #
        # p_id = Persona.objects.raw('select id from main.Persona where nome = %s and cognome = %s and email = %s and telefono = %s and password = %s;', [nome, cognome, email, telefono, password])
        #
        # cursor_c = connection.cursor()
        # cursor_c.execute('insert into main.Cliente(id) values(%s);', [p_id[0].id])

        # senza raw query
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

        # con raw query
        # cursor_c = connection.cursor()
        # cursor_c.execute('insert into main.Cocktail(nome, ingredienti, prezzo) values(%s, %s, %s);', [nomeCocktail, ingredienti, prezzo])
        #
        # cocktail = Cocktail.objects.raw('select * from main.Cocktail where nome = %s and ingredienti = %s and prezzo = %s;', [nomeCocktail, ingredienti, prezzo])
        #
        # cursor_bgc = connection.cursor()
        # cursor_bgc.execute('insert into main.Barista_gestisce_cocktail(fk_id_cocktail, fk_id_barista, azione) values(%s, %s, %s);', [cocktail[0].id, barista_id, 'Inserimento'])

        # senza raw query
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

        # con raw query
        # cursor_c = connection.cursor()
        # cursor_bgc = connection.cursor()
        #
        # if ingredienti and prezzo:
        #     cursor_c.execute('update main.Cocktail set ingredienti = %s, prezzo = %s where id = %s;', [ingredienti, prezzo, cocktail_id])
        #
        #     cursor_bgc.execute('insert into main.Barista_gestisce_cocktail(fk_id_cocktail, fk_id_barista, azione) values(%s, %s, %s);', [cocktail_id, barista_id, 'Modifica'])
        #     # print('aggiorna entrambi')
        # elif not prezzo and ingredienti:
        #     cursor_c.execute('update main.Cocktail set ingredienti = %s where id = %s;', [ingredienti, cocktail_id])
        #
        #     cursor_bgc.execute('insert into main.Barista_gestisce_cocktail(fk_id_cocktail, fk_id_barista, azione) values(%s, %s, %s);', [cocktail_id, barista_id, 'Modifica'])
        #     # print('aggiorna ingredienti')
        # elif not ingredienti and prezzo:
        #     cursor_c.execute('update main.Cocktail set prezzo = %s where id = %s;', [prezzo, cocktail_id])
        #
        #     cursor_bgc.execute('insert into main.Barista_gestisce_cocktail(fk_id_cocktail, fk_id_barista, azione) values(%s, %s, %s);', [cocktail_id, barista_id, 'Modifica'])
        #     # print('aggiorna prezzo')
        # elif not ingredienti and not prezzo:
        #     print('non aggiornare nulla')
        #
        # c = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [cocktail_id])
        # context = {
        #     'cocktail': c[0],
        #     'barista_id': barista_id,
        # }

        # senza raw query
        barista = Barista.objects.get(id=barista_id)
        c = Cocktail.objects.get(id=cocktail_id)
        if ingredienti and prezzo:
            c.ingredienti = ingredienti
            c.prezzo = prezzo
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            # print('aggiorna entrambi')
        elif not prezzo and ingredienti:
            c.ingredienti = ingredienti
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            # print('aggiorna ingredienti')
        elif not ingredienti and prezzo:
            c.prezzo = prezzo
            c.save()

            barista_gestisce_cocktail = BaristaGestisceCocktail(fk_id_cocktail=c, fk_id_barista=barista, azione='Modifica')
            barista_gestisce_cocktail.save()
            # print('aggiorna prezzo')
        elif not ingredienti and not prezzo:
            print('non aggiornare nulla')

        c = Cocktail.objects.get(id=cocktail_id)
        context = {
            'cocktail': c,
            'barista_id': barista_id,
        }

        return render(request, 'bar/modifica-avvenuta.html', context)


def ordinazioneCocktail(request, cliente_id, cocktail_id):
    # con raw query
    # c = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [cocktail_id])
    #
    # o = {
    #     'id': c[0].id,
    #     'nome': c[0].nome,
    #     'prezzo': c[0].prezzo,
    # }
    #
    # global ordine
    # ordine = ordina(o)
    #
    # context = {
    #     'c': c[0],
    #     'cliente_id': cliente_id,
    # }

    # senza raw query
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

    # con raw query
    # cursor_cp = connection.cursor()
    # cursor_cp.execute('insert into main.Codice_prenotazione(codice) values(%s);', [codice])
    #
    # codice_prenotazione = CodicePrenotazione.objects.raw('select id from main.Codice_prenotazione where codice = %s;', [codice])
    #
    # for o in ordine:
    #     cursor_o = connection.cursor()
    #     cursor_o.execute('insert into main.Cliente_ordina_cocktail_ricevendo_codice_prenotazione(data, fk_id_cocktail, fk_id_codice_prenotazione, fk_id_cliente) '
    #                      'values(%s, %s, %s, %s);', [today, o['id'], codice_prenotazione[0].id, cliente_id])

    # senza raw query
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
    # con raw query
    # c = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [cocktail_id])
    # nome = c[0].nome
    # cursor = connection.cursor()
    # cursor.execute('delete from main.Cocktail where id = %s;', [cocktail_id])

    # senza raw query
    c = Cocktail.objects.get(id=cocktail_id)
    nome = c.nome
    c.delete()

    context = {
        'nome': nome,
        'barista_id': barista_id,
    }
    return render(request, 'bar/elimina-cocktail.html', context)


def controlloCodice(request, barista_id, codice_id):
    # con raw query
    # codice = CodicePrenotazione.objects.raw('select * from main.Codice_prenotazione where id = %s;', [codice_id])
    # cursor = connection.cursor()
    # cursor.execute('update main.Codice_prenotazione set fk_id_barista = %s where id = %s;', [barista_id, codice_id])
    #
    # list_cocktails = ClienteOrdinaCocktailRicevendoCodicePrenotazione.objects.raw('select * from main.Cliente_ordina_cocktail_ricevendo_codice_prenotazione where id = %s;', [codice_id])
    #
    # cocktails = []
    #
    # for c in list_cocktails:
    #     cocktail = Cocktail.objects.raw('select * from main.Cocktail where id = %s;', [c.fk_id_cocktail.id])
    #     cocktails.append({
    #         'nome': cocktail[0].nome,
    #         'ingredienti': cocktail[0].ingredienti,
    #     })
    #
    # context = {
    #     'barista_id': barista_id,
    #     'codice': codice[0],
    #     'list_cocktails': cocktails,
    # }

    # senza raw query
    codice = CodicePrenotazione.objects.get(id=codice_id)
    barista = Barista.objects.get(id=barista_id)

    codice.fk_id_barista = barista
    codice.save()

    list_cocktails = ClienteOrdinaCocktailRicevendoCodicePrenotazione.objects.filter(fk_id_codice_prenotazione=codice_id)

    cocktails = []

    for c in list_cocktails:
        cocktail = Cocktail.objects.get(id=c.fk_id_cocktail.id)
        cocktails.append({
            'nome': cocktail.nome,
            'ingredienti': cocktail.ingredienti,
        })

    context = {
        'barista_id': barista_id,
        'codice': codice,
        'list_cocktails': cocktails,
    }

    return render(request, 'bar/controllo-codice.html', context)




