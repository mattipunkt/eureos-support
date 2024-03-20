from django import forms

CHOICES = (('Windows', 'Windows'),('Handy', 'Handy'),('DATEV', 'DATEV'), ('Microsoft Office', 'Microsoft Office'), ('Hardwareprobleme', 'Hardwareprobleme'), ('Remote-Work / VPN', 'Remote-Work / VPN'), ('ELO', 'ELO'), ('Anderes', 'Anderes'))


class createTicketForm(forms.Form):
    name = forms.CharField(label='Vor- und Nachname', max_length=255)
    mail_adress = forms.CharField(label="Ihre eureos-Mail-Adresse", max_length=255)
    problem = forms.ChoiceField(choices=CHOICES)
    title = forms.CharField(label="Betreff des Tickets", max_length=255)
    description = forms.CharField(label="Bitte beschreiben Sie ihr Problem", widget=forms.Textarea(), max_length=20000)


class addMessage(forms.Form):
    message = forms.CharField(label="Bitte geben Sie ihre Nachricht ein", widget=forms.Textarea(), max_length=2000)


class loginForm(forms.Form):
    username = forms.CharField(label="eureos Mail-Adresse zum Anmelden", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class createUser(forms.Form):
    first_name = forms.CharField(label="Vornamen eingeben", max_length=60)
    last_name= forms.CharField(label="Nachnamen eingeben", max_length=60)
    username = forms.CharField(label="Mail-Adresse zum Anmelden eingeben", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class passwordReset(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)

class changeCategory(forms.Form):
    new_problem = forms.ChoiceField(choices=CHOICES)
