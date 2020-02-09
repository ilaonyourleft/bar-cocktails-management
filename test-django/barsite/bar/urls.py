from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomepageView.as_view(), name='home'),
    path('area-riservata/', views.login, name='login'),
    path('registrazione/', views.registrazione, name='registrazione'),
    # path('ordinazione/', views.login, name='login'),
    path('codice-prenotazione/', views.codicePrenotazione, name='codice-prenotazione'),
    # path('modifica-menu/', views.login, name='login'),
    path('inserisci-cocktail/', views.inserisciCocktail, name='inserisci-cocktail'),
    path('controllo-codice/', views.controlloCodice, name='controllo-codice'),
]
