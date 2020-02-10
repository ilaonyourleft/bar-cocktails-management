from django.db import models


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Persona(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.BigIntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        # managed = False
        db_table = 'Persona'

    # def __str__(self):
    #     return 'id: ' + str(self.id) + ', nome: ' + self.nome + ', cognome: ' \
    #            + self.cognome + ', email: ' + self.email + ', telefono: ' + str(self.telefono) \
    #            + ', password: ' + self.password
    #
    #     return {
    #         'id': str(self.id),
    #         'nome': self.nome,
    #         'cognome': self.cognome,
    #         'email': self.email,
    #         'telefono': str(self.telefono),
    #         'password': self.password,
    #     }


class Barista(models.Model):
    id = models.OneToOneField(Persona,
                              db_column='id',
                              primary_key=True,
                              on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Barista'


class Cliente(models.Model):
    id = models.OneToOneField(Persona,
                              db_column='id',
                              primary_key=True,
                              on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Cliente'


class Cocktail(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    ingredienti = models.TextField()  # This field type is a guess.
    prezzo = models.FloatField()

    class Meta:
        # managed = False
        db_table = 'Cocktail'

    def __str__(self):
        return 'id: ' + str(self.id) + ', nome: ' + self.nome + ', ingredienti: ' \
               + self.ingredienti + ', prezzo: ' + str(self.prezzo)


class BaristaGestisceCocktail(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_id_barista = models.ForeignKey(Barista,
                                      db_column='fk_id_barista',
                                      on_delete=models.CASCADE)
    fk_id_cocktail = models.ForeignKey(Cocktail,
                                       db_column='fk_id_cocktail',
                                       on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Barista_gestisce_cocktail'


class CodicePrenotazione(models.Model):
    id = models.BigAutoField(primary_key=True)
    codice = models.BigIntegerField()
    fk_id_barista = models.ForeignKey(Barista,
                                      db_column='fk_id_barista',
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Codice_prenotazione'


class ClienteOrdinaCocktailRicevendoCodicePrenotazione(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.CharField(max_length=100)
    fk_id_cliente = models.ForeignKey(Cliente,
                                      db_column='fk_id_cliente',
                                      on_delete=models.CASCADE)
    fk_id_cocktail = models.ForeignKey(Cocktail,
                                       db_column='fk_id_cocktail',
                                       on_delete=models.CASCADE)
    fk_id_codice_prenotazione = models.ForeignKey(CodicePrenotazione,
                                                  db_column='fk_id_codice_prenotazione',
                                                  on_delete=models.CASCADE)

    class Meta:
        # managed = False
        db_table = 'Cliente_ordina_cocktail_ricevendo_codice_prenotazione'
