from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createTicket/', views.createTicket, name='createTicket'),
#    path('pushData/', views.getData, name='pushData')
]
