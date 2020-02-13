from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('', views.goToHomepage, name='goToHomepage'),
    path('', views.logout, name='logout'),
    path('area-riservata/', views.login, name='login'),
    path('registrazione/', views.goToRegistrazione, name='goToRegistrazione'),
    path('registrazione-avvenuta', views.registrazione, name='registrazione'),

    # CLIENTE
    path('ordinazione/<int:cliente_id>/', views.goToOrdinazione, name='goToOrdinazione'),
    path('ordinazione-cocktail/<int:cliente_id>/<int:cocktail_id>/', views.ordinazioneCocktail, name='ordinazione-cocktail'),
    path('ordinazione-avvenuta/<int:cliente_id>/', views.confermaOrdinazione, name='conferma-ordinazione'),
    #path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),
    path('storico/<int:cliente_id>/', views.goToStorico, name='storico'),

    # BARISTA
    # --- MODIFICA
    path('modifica-menu/', views.goToModificaMenu, name='goToModificaMenu'),
    path('modifica-cocktail/<int:cocktail_id>/', views.goToModificaCocktail, name='goToModificaCocktail'),
    path('modifica-avvenuta/<int:cocktail_id>/', views.modificaCocktail, name='modifica-cocktail'),
    # --- INSERIMENTO
    path('inserisci-cocktail/', views.goToInserisciCocktail, name='goToInserisciCocktail'),
    path('inserimento-avvenuto/', views.inserisciCocktail, name='inserisci-cocktail'),
    # --- CANCELLAZIONE
    path('elimina-cocktail/<int:cocktail_id>/', views.eliminaCocktail, name='eliminaCocktail'),
    # --- CONTROLLO CODICE
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
    path('codice-prenotazione/<int:barista_id>/', views.codicePrenotazione, name='codice-prenotazione')
]
