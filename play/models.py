from django.db import models
 
class Equipement(models.Model):
    id = models.CharField(max_length=100 , primary_key= True)
    disponibilite = models.CharField(max_length=20)
    capacite = models.IntegerField() 
    photo = models.CharField(max_length=200)
    # Autres champs spécifiques à l'équipement (ex: type, description)

    def __str__(self):
        return self.id


class Character(models.Model):
    nom = models.CharField(max_length=100 , primary_key= True)
    etat = models.CharField(max_length=20) 
    type = models.CharField(max_length=20 )
    photo = models.CharField(max_length=200)
    lieu = models.ForeignKey(Equipement, on_delete=models.SET_NULL, null=True)
    inventaire = models.JSONField(default=list)

    def __str__(self):
        return self.nom


