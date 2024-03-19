from django.db import models

# Create your models here.
class Ticket(models.Model):
    email = models.CharField(default="dummy@eureos.de", max_length=255)
    problemtype = models.CharField(default="KeinProblemGewählt", max_length=400)
    problemdescription = models.CharField(default="Keine Beschreibung gegeben.", max_length=20000)
