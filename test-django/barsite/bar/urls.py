from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('area-riservata/', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('registrazione/', views.registrazione, name='registrazione'),

    # CLIENTE
    path('ordinazione/', views.login, name='ordinazione'),
    path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),

    # BARISTA
    path('modifica-menu/', views.login, name='modifica-menu'),
    path('inserisci-cocktail/', views.inserisciCocktail, name='inserisci-cocktail'),
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
]
