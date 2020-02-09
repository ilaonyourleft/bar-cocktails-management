from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('registrazione/', views.registrazione, name='registrazione'),
    path('ordinazione/', views.ordinazione, name='ordinazione'),
    path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),
    path('modifica-menu/', views.modificaMenu, name='modifica-menu'),
    path('inserisci-cocktail/', views.inserisciCocktail, name='inserisci-cocktail'),
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
]
