from django.db import models

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(default="DummyTitle", max_length=255)
    email = models.CharField(default="dummy@eureos.de", max_length=255)
    name = models.CharField(default="Max Mustermann", max_length=255)
    problemtype = models.CharField(default="KeinProblemGewählt", max_length=400)
    problemdescription = models.CharField(default="Keine Beschreibung gegeben.", max_length=20000)
    created_on = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)


class Message(models.Model):
    content = models.TextField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    added_by = models.CharField(default="Max Mustermann", max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
