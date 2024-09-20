from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('contact', views.Contact, name='contact'),
    path('portal', views.Portal, name='portal'),
    path('sign-up', views.SignUp, name='sign_up'),
    path('sign-in', views.SignIn, name='sign_in'),
    path('sign-out', views.SignOut, name='sign-out'),
]
