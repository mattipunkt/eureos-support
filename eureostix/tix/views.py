from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect


from . import forms
from .models import Ticket, Message

from .mailservice import sendmail

# Create your views here.
def index(request):
    return render(request, "index.html")

def createTicket(request):
    if request.method == 'POST':
        form = forms.createTicketForm(request.POST)
        name = request.POST.get('name')
        mail_adress = request.POST.get('mail_adress')
        problem = request.POST.get('problem')
        description = request.POST.get('description')
        title = request.POST.get('title')
        if form.is_valid():
            print("POST-Erhalten:\nMail: " + mail_adress + "\nProblem: " + problem + "\nBeschreibung: " + description)

            ticket = Ticket.objects.create(email=mail_adress, problemtype=problem, problemdescription=description, title=title, name=name)
            ticket.save()
            ticket_id = ticket.id
            mail_content = "Hallo " + name + ",\n\nSie haben erfolgreich das Ticket beim eureos-Support angelegt. Wir werden uns so schnell wie es geht um Ihr anliegen kuemmern.\nSie koennen das Ticket unter folgender Adresse aufrufen:\n\n http://localhost:8000/ticket/" + str(ticket_id) + "\n\nSobald sich etwas am Status des Tickets aendert, bekommen Sie eine weitere Mail."
            sendmail(mail_adress, mail_content, "Ticket wurde erstellt! ID: " + str(ticket_id))
            print("Mail wurde gesendet an " + mail_adress)
            return render(request, "success.html")
            
    else:
        form = forms.createTicketForm()

    return render(request, "createticket.html", {"form": form})


def ticketRedirecter(request):
    return render(request, "ticketredirect.html")


def viewTicket(request, id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=id)
        getMessage = request.POST.get('message')
        message = Message.objects.create(content=getMessage, ticket=ticket)
        return redirect('/ticket/'+ str(id))
    else:
        addMessageForm = forms.addMessage()
        ticket = Ticket.objects.get(pk=id)
        messages = Message.objects.filter(ticket=ticket)
        return render(request, "ticketview.html", {
            "id": id,
            "ticket": ticket,
            "addMessageForm": addMessageForm,
            "messages": messages,
            })

def closeTicket(request, id):
        print('Schließe Ticket mit der ID' + str(id))
        ticket = Ticket.objects.get(pk=id)
        ticket.open = False
        ticket.save()
        return redirect('/ticket/' + str(id))


