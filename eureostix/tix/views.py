from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect


from . import forms
from .models import Ticket

# Create your views here.
def index(request):
    return render(request, "index.html")

def createTicket(request):
    if request.method == 'POST':
        form = forms.createTicketForm(request.POST)
        mail_adress = request.POST.get('mail_adress')
        problem = request.POST.get('problem')
        description = request.POST.get('description')
        if form.is_valid():
            print("POST-Erhalten:\nMail: " + mail_adress + "\nProblem: " + problem + "\nBeschreibung: " + description)
            ticket = Ticket.objects.create(email=mail_adress, problemtype=problem, problemdescription=description)
            return render(request, "success.html")
            
    else:
        form = forms.createTicketForm()

    return render(request, "createticket.html", {"form": form})


def viewTicket(request, id):
    return render(request, "ticketview.html")
