from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from bar.models import Cocktail, Persona, Cliente, Barista
from bar.forms import Registrazione


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


def codicePrenotazione(request):
    return HttpResponse('Pagina di codice prenotazione.')


def inserisciCocktail(request):
    return HttpResponse('Pagina di inserimento cocktail.')


def controlloCodice(request):
    return HttpResponse('Pagina di controllo codice prenotazione.')
