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
    path('storico/<int:cliente_id>/', views.goToStorico, name='storico'),

    # BARISTA
    # --- MODIFICA
    path('modifica-menu/<int:barista_id>/', views.goToModificaMenu, name='goToModificaMenu'),
    path('modifica-cocktail/<int:barista_id>/<int:cocktail_id>/', views.goToModificaCocktail, name='goToModificaCocktail'),
    path('modifica-avvenuta/<int:barista_id>/<int:cocktail_id>/', views.modificaCocktail, name='modifica-cocktail'),
    # --- INSERIMENTO
    path('inserisci-cocktail/<int:barista_id>/', views.goToInserisciCocktail, name='goToInserisciCocktail'),
    path('inserimento-avvenuto/<int:barista_id>/', views.inserisciCocktail, name='inserisci-cocktail'),
    # --- CANCELLAZIONE
    path('elimina-cocktail/<int:barista_id>/<int:cocktail_id>/', views.eliminaCocktail, name='eliminaCocktail'),
    # --- CONTROLLO CODICE
    path('controllo-codice/<int:barista_id>/<int:codice_id>/', views.controlloCodice, name='controllo-codice'),
    path('codice-prenotazione/<int:barista_id>/', views.goToCodicePrenotazione, name='codice-prenotazione'),
]
