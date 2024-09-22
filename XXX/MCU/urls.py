from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('contact', views.Contact, name='contact'),
    path('portal', views.Portal, name='portal'),
    path('sign-up', views.SignUp, name='sign_up'),
    path('sign-in', views.SignIn, name='sign_in'),
    path('sign-out', views.SignOut, name='sign_out'),
    path('dashboard-user', views.DashboardUser, name='dashboard_user'),
    path('dashboard-doctor', views.DashboardDoctor, name='dashboard_doctor'),
    path('request-rejected', views.RequestRejected, name='request_rejected'),
    path('doctor-management', views.DoctorManagement, name='doctor_management'),
    path('create-doctor', views.CreateDoctor, name='create_doctor'),
    path('belum', views.Belum, name='belum'),
]
