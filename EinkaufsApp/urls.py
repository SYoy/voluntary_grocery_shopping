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
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # public urls
    path('', views.start, name='start'),
    path('faq', views.faq, name='faq'),
    path('impressum', views.impressum, name='impressum'),
    path('local', views.local, name='local'),
    path('datenschutz', views.datenschutz, name='datenschutz'),
    path('schwarzes_brett_public/', views.helfen_voransicht, name='public_blackboard'),
    path('get/ajax/listings', views.listings, name="query_listings_blackboard"),

    # account related urls
    path('registrieren_helfender/', views.signupHelper, name='signup_helper'),
    path('registrieren_empfaenger/', views.signupInNeed, name='signup_inneed'),
    url(r'^anmelden/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    url(r'^abmelden/$', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path(r'abmelden/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),

    # pw reset
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    # home view
    path('home/', views.home, name='home'),

    # app InNeed
    path('einkauf/', views.einkaufsliste, name='einkaufsliste'),
    path('post/ajax/setInactive', views.setInactive, name="setInactive"),
    path('post/ajax/setDone', views.setDone, name="setDone"),

    # app Helper
    path('schwarzes_brett/', views.helfen, name='blackboard'),
    path('helfer_einkaufslisten/', views.helfer_einkaufslisten, name='helfer_einkaufslisten'),
    path('post/ajax/setInWork', views.setInWork, name="setInWork"),
    path('post/ajax/getAccepted', views.getAccepted, name="getAccepted"),

    # admin
    path('admin/', admin.site.urls),
]