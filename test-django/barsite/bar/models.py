from django.db import models


# Create your models here.

class Barista(models.Model):
    id = models.OneToOneField('Persona', models.DO_NOTHING, db_column='id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'barista'


class BaristaGestisceCocktail(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_id_barista = models.ForeignKey(Barista, models.DO_NOTHING, db_column='fk_id_barista')
    fk_id_cocktail = models.ForeignKey('Cocktail', models.DO_NOTHING, db_column='fk_id_cocktail')

    class Meta:
        managed = False
        db_table = 'barista_gestisce_cocktail'


class Cliente(models.Model):
    id = models.OneToOneField('Persona', models.DO_NOTHING, db_column='id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class ClienteOrdinaCocktailRicevendoCodicePrenotazione(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.CharField(max_length=100)
    fk_id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='fk_id_cliente')
    fk_id_cocktail = models.ForeignKey('Cocktail', models.DO_NOTHING, db_column='fk_id_cocktail')
    fk_id_codice_prenotazione = models.ForeignKey('CodicePrenotazione', models.DO_NOTHING,
                                                  db_column='fk_id_codice_prenotazione')

    class Meta:
        managed = False
        db_table = 'cliente_ordina_cocktail_ricevendo_codice_prenotazione'


class Cocktail(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    ingredienti = models.TextField()  # This field type is a guess.
    prezzo = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cocktail'


class CodicePrenotazione(models.Model):
    id = models.BigAutoField(primary_key=True)
    codice = models.BigIntegerField()
    fk_id_barista = models.ForeignKey(Barista, models.DO_NOTHING, db_column='fk_id_barista', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codice_prenotazione'


class Persona(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.BigIntegerField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return 'id: ' + str(self.id) + ', nome: ' + self.nome + ', cognome: ' \
               + self.cognome + ', email: ' + self.email + ', telefono: ' + str(self.telefono) \
               + ', password: ' + self.password

    class Meta:
        managed = False
        db_table = 'persona'
