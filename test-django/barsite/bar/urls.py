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
    path('ordinazione/', views.login, name='ordinazione'),
    path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),

    # BARISTA
    path('modifica-menu/', views.goToModificaMenu, name='goToModificaMenu'),
    path('modifica-cocktail/<int:cocktail_id>/', views.goToModificaCocktail, name='goToModificaCocktail'),
    path('inserisci-cocktail/', views.goToInserisciCocktail, name='goToInserisciCocktail'),
    path('inserimento-avvenuto/', views.inserisciCocktail, name='inserisci-cocktail'),
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
]
