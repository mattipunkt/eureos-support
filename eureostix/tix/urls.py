from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createTicket/', views.createTicket, name='createTicket'),
    path('viewticket/', views.ticketRedirecter, name="ticketRedirect"),
    path('ticket/<int:id>/', views.viewTicket, name="ticketViewer"),
    path('ticket/<int:id>/close/', views.closeTicket, name="closeTicket"),
    path('login/', views.loginPage, name="closeTicket"),
    path('logout/', views.logoutAction, name="logoutAction"),
    path('backend/', views.adminBackend, name="adminBackend"),
    path('createUser/', views.createUser, name="createUser"),
    path('deleteUser/<int:id>/', views.deleteUser, name="deleteUser"),
    path('resetPassword/<int:id>/', views.resetPassword, name="resetPassword"),
#    path('pushData/', views.getData, name='pushData')
]
