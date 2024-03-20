from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Django Users
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model

# Django Forms
from . import forms
from .models import Ticket, Message

# Mail-Function to send mails
from .mailservice import sendmail, checkmails

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
        if request.user.is_authenticated:
            username = request.user.first_name + ' ' + request.user.last_name
        else:
            username = "Max Mustermann"
        
        message = Message.objects.create(content=getMessage, ticket=ticket, added_by=username)
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
            "changeCategory": forms.changeCategory,
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


# ACCOUNT STUFF
def loginPage(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "auth/misinput.html")
    else:
        form = forms.loginForm()
        return render(request, "auth/login.html", {
            "loginform": form
        })
    

def logoutAction(request):
    logout(request)
    return redirect('/')


def adminBackend(request):
    checkmails()
    User = get_user_model()
    users = User.objects.all()
    opentickets = Ticket.objects.filter(open=True)
    closedtickets = Ticket.objects.filter(open=False)
    return render(request, 'adminbackend.html', {
        "createUserForm": forms.createUser(),
        "passwordReset": forms.passwordReset(),
        "users": users,
        "opentickets": opentickets,
        "closedtickets": closedtickets,
    })


def createUser(request):
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    password = request.POST.get('password')
    user = User.objects.create_user(username, username, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return HttpResponse('<script>alert("Erfolgreich! Nutzer wurde angelegt.");window.location.replace("/backend");</script>')



def deleteUser(request, id):
    if request.user.is_authenticated:
            if not request.user.id == id:
                u = User.objects.get(pk=id)
                u.delete()
                print("Nutzer gelöscht.")
                return HttpResponse('<script>alert("Erfolgreich! Der Nutzer wurde erfolgreich gelöscht!");window.location.replace("/backend");</script>')
            else: 
                print('Nutzer nicht gelöscht. Nutzer hat versucht sich selbst zu löschen!')
                return HttpResponse('<script>alert("Fehler! Du hast versucht dich selbst zu löschen. Das geht nicht!");window.location.replace("/backend");</script>')

def resetPassword(request, id):
    if request.user.is_authenticated:
        new_password = request.POST.get('new_password')
        u = User.objects.get(pk=id)
        u.set_password = new_password
        u.save()
        return HttpResponse('<script>alert("Erfolgreich! Das Passwort wurde geändert.");window.location.replace("/backend");</script>')


def changeTicketCategory(request, id):
    if request.user.is_authenticated:
        ticket = Ticket.objects.get(pk=id)
        new_category = request.POST.get('new_problem')
        ticket.problemtype = new_category
        ticket.save()
        return HttpResponse('<script>alert("Erfolgreich! Die Kategorie wurde geändert.");window.location.replace("/ticket/'+str(id)+'");</script>')