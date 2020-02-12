from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('area-riservata/', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('registrazione/', views.goToRegistrazione, name='goToRegistrazione'),
    path('registrazione-avvenuta', views.registrazione, name='registrazione'),
    path('', views.goToHomepage, name='goToHomepage'),

    # CLIENTE
    path('ordinazione/', views.goToOrdinazione, name='goToOrdinazione'),
    ##path('ordinazione-effettiva/', views.goToOrdinazione, name='goToOrdinazione'),
    path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),

    # BARISTA
    # --- MODIFICA
    path('modifica-menu/', views.goToModificaMenu, name='goToModificaMenu'),
    path('modifica-cocktail/<int:cocktail_id>/', views.goToModificaCocktail, name='goToModificaCocktail'),
    path('modifica-avvenuta/<int:cocktail_id>/', views.modificaCocktail, name='modifica-cocktail'),
    # --- INSERIMENTO
    path('inserisci-cocktail/', views.goToInserisciCocktail, name='goToInserisciCocktail'),
    path('inserimento-avvenuto/', views.inserisciCocktail, name='inserisci-cocktail'),
    # --- CANCELLAZIONE
    # --- CONTROLLO CODICE
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
]
