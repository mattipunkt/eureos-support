from django import forms


class createTicketForm(forms.Form):
    mail_adress = forms.CharField(label="Ihre eureos-Mail-Adresse", max_length=255)
    CHOICES = (('Windows', 'Windows'),('Handy', 'Handy'),('DATEV', 'DATEV'), ('Microsoft Office', 'Microsoft Office'), ('Hardwareprobleme', 'Hardwareprobleme'))
    problem = forms.ChoiceField(choices=CHOICES)
    title = forms.CharField(label="Betreff des Tickets", max_length=255)
    description = forms.CharField(label="Bitte beschreiben Sie ihr Problem", widget=forms.Textarea(), max_length=2000)