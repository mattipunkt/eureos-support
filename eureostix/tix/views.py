from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def createTicket(request):
    return render(request, "createticket.html")


def getData(request):
    if request.method == 'GET':
        return HttpResponse('Error!')
    elif request.method == 'POST':
        email = request.POST.get('')
