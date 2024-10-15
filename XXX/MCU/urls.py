from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('contact', views.Contact, name='contact'),
    path('sign-in', views.SignIn, name='signIn'),
    path('sign-up', views.SignUp, name='signUp'),
    path('sign-out', views.SignOut, name='signOut'),
    path('dashboard', views.Dashboard, name='dashboard'),
    path('mcu/dashboard', views.UserDashboard, name='UserDashboard'),
    path('mcu/regis', views.regisMCU, name='regisMcu'),
    path('mcu/update', views.updateRegis, name='updateRegis'),
    path('mcu/delete', views.deleteRegis, name='deleteRegis'),
    path('mcu/history', views.UserHistory, name='UserHistory'),
    path('doctor/dashboard', views.DoctorDashboard, name='DoctorDashboard'),
    path('doctor/history', views.DoctorHistory, name='DoctorHistory'),
    path('doctor/finish', views.finishMCU, name='finishMcu'),
    path('doctor/update', views.updateMCU, name='updateMcu'),
]
