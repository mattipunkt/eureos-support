from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createTicket/', views.createTicket, name='createTicket'),
    path('viewticket/', views.ticketRedirecter, name="ticketRedirect"),
    path('ticket/<int:id>', views.viewTicket, name="ticketViewer"),
#    path('pushData/', views.getData, name='pushData')
]
