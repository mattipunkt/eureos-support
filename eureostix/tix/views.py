from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Django Forms
from . import forms
from .models import Ticket, Message

# Mail-Function to send mails
from .mailservice import sendmail

# env-stuff
import os
from dotenv import load_dotenv

load_dotenv() 

HOST_URL = os.getenv('HOST_URL')


# Create your views here.
def index(request):
    return render(request, "index.html")

def createTicket(request):
    if request.method == 'POST':
        # form to create a new ticket
        form = forms.createTicketForm(request.POST)

        # form-values
        name = request.POST.get('name')
        mail_adress = request.POST.get('mail_adress')
        problem = request.POST.get('problem')
        description = request.POST.get('description')
        title = request.POST.get('title')

        if form.is_valid():
            print("POST-Erhalten:\nMail: " + mail_adress + "\nProblem: " + problem + "\nBeschreibung: " + description)
            ticket = Ticket.objects.create(email=mail_adress, problemtype=problem, problemdescription=description, title=title, name=name)
            ticket.save()

            # Send Mail for new Ticket
            mail_content = "Hallo " + name + ",\n\nSie haben erfolgreich das Ticket beim eureos-Support angelegt. Wir werden uns so schnell, wie es geht um Ihr anliegen kuemmern.\nSie koennen das Ticket unter folgender Adresse aufrufen:\n\n "+HOST_URL+"/ticket/" + str(ticket.id) + "\n\nDaneben koennen Sie das Ticket aufrufen in dem Sie die Ticket-Nummer (" + str(ticket.id) + ") über die Funktion 'Ticket einsehen' im oberen Reiter auf der Support-Seite eingeben. \n\nSobald sich etwas am Status des Tickets aendert, bekommen Sie eine weitere Mail.\n\nIhr eureos IT-Support :)"
            sendmail(mail_adress, mail_content, "Ticket wurde erstellt! ID: " + str(ticket.id))
            print("Mail wurde gesendet an " + mail_adress)

            # redirect to success page
            return render(request, "success.html")
            
    else: # render Create Tickets Form
        form = forms.createTicketForm()

    return render(request, "createticket.html", {"form": form})

# Ticket-Redirecter consists of an input-field to just redirect to the ticket-number, which was sent to
# the ticket creator
def ticketRedirecter(request):
    return render(request, "ticketredirect.html")

# view ticket function does many things:
#   - it views all things belonging to one ticket including messages
#   - it sends an email if anything in the ticket changes
def viewTicket(request, id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=id)
        # get Comment on the Ticket to process
        getMessage = request.POST.get('message')

        
        message = Message.objects.create(content=getMessage, ticket=ticket)
        message.save()
        

        # Send Mail with ticket number
        sendmail(ticket.email, "Hallo " + ticket.name + "\n\nEs gibt eine neue Nachricht im eureos Ticket-System.\n\n"+message.added_by+" hat um "+str(message.created_on)+" folgende Nachricht hinzugefuegt: \n\n"+getMessage+"\n\nSie koennen unter folgender Adresse Ihr Ticket wieder aufrufen.\n\n"+HOST_URL+"/ticket/" + str(ticket.id) + "\n\nWICHTIG: Wenn Sie der Meinung sind, dass wir Ihr Anliegen gelöst haben, dann schließen Sie bitte das Ticket. Dabei ist zu beachten, dass danach in den 'Nur-Lesen'-Zustand wechselt und nicht mehr bearbeitet werden kann.\n\nIhr eureos IT-Support :)", "Neue Nachricht auf Ihrem Ticket! (ID: "+str(ticket.id)+")")
        print("Mail wurde gesendet an " + ticket.email)

        return redirect('/ticket/'+ str(id)+"/")

    else:
        # Just display the ticket-stuff
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

        mail_content = "Hallo " + ticket.name + ",\n\nDas Ticket, das Sie erstellt haben, mit dem Titel '" + ticket.title + "', wurde von uns bearbeitet und geschlossen und kann jetzt nicht weiter bearbeitet werden. Wenn weiterhin unklarheiten bestehen, dann wenden Sie sich bitte telefonisch an uns. \n\nZur Info: Sie koennen das Ticket weiterhin aufrufen und die Konversation anschauen.\n\nIhr eureos IT-Support :)"
        sendmail(ticket.email, mail_content, "Ticket wurde geschlossen! (ID: " + str(ticket.id)+ ")")
        print("Mail wurde gesendet an " + ticket.email)
        return redirect('/ticket/' + str(id))


