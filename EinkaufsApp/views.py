from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from EinkaufsApp.backend_forms.forms_signup import SignUpForm

def start(request):
    return render(request, 'public/start.html')

def signupHelper(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.location = form.cleaned_data.get('location')
            user.person.group = 'H'
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/registrationHelper.html', {'form': form})

def signupInNeed(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.person.location = form.cleaned_data.get('location')
            user.person.group = 'E'
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = SignUpForm()
    return render(request, 'accounts/registrationInNeed.html', {'form': form})

@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'public/home.html', {'group': request.user.person.group, 'username': request.user.username})
    else:
        return HttpResponse("Sie sind nicht angemeldet")

@login_required
def einkaufsliste(request):
    return HttpResponse("Einkaufslisten erstelln todo")

@login_required
def helfen(request):
    return HttpResponse("Schwarzes brett Todo")

def helfen_voransicht(request):
    return render(request, 'public/preview_blackboard.html')

def faq(request):
    return HttpResponse("FAQ Todo")


# def custom_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             # form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#
#             # check user group
#             if user is not None:
#                 user.refresh_from_db()
#                 if user.person.group == 'E':
#                     return redirect('home', {'group': 'Empfaenger'})
#                 elif user.person.group == 'H':
#                     return redirect('home', {'group': 'Helfender'})
#             else:
#                 form = AuthenticationForm()
#                 return render(request, 'accounts/login.html', {'form': form})
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})