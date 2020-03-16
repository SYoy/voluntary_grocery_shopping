"""EinkaufsApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('schwarzes_brett', views.helfen_voransicht, name='public_blackboard'),

    path('registrieren_helfender/', views.signupHelper, name='signup_helper'),
    path('registrieren_empfaenger/', views.signupInNeed, name='signup_inneed'),
    url(r'^anmelden/$', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    url(r'^abmelden/$', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path(r'abmelden/', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),

    path('home/', views.home, name='home'),
    path('einkauf', views.einkaufsliste, name='einkaufsliste'),
    path('helfen/', views.helfen, name='helfen'),

    path('admin/', admin.site.urls),
]