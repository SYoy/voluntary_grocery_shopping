# Core
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# AJAX
from django.http import JsonResponse
from django.core import serializers

# Forms
from EinkaufsApp.backend_forms.forms_signup import SignUpForm
from EinkaufsApp.backend_forms.forms_einkaufliste import EinkaufsauftragForm
from EinkaufsApp.backend_forms.forms_blackboard import SelectionForm

# Models for Queries
from EinkaufsApp.models import Einkaufsauftrag

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
    if request.user.is_authenticated and request.user.person.group in ["E", "D", "S"]:
        if request.method == 'POST':
            form = EinkaufsauftragForm(request.POST)
            if form.is_valid():
                auftrag = form.save()
                auftrag.refresh_from_db()

                # Aus Online Form uebernehmen
                auftrag.nachricht = form.cleaned_data.get('nachricht')
                auftrag.liste_text = form.cleaned_data.get('liste_text')
                auftrag.telefonnummer = form.cleaned_data.get('telefonnummer')
                auftrag.budget = form.cleaned_data.get('budget')

                # Beim Erstellen hinzugefuegt
                auftrag.status = "aktiv"
                auftrag.auftragsdatum = timezone.now()
                auftrag.user_id = request.user.id

                auftrag.save()
                # message - bzw. Auftrag bestätigen
                return render(request, 'app/app_inneed.html', {'form': form})
        else:
            form = EinkaufsauftragForm(request.POST)
        return render(request, 'app/app_inneed.html', {'form': form})

    elif request.user.is_authenticated and request.user.person.group == "H":
        messages.add_message(request, messages.INFO, 'Sie sind als Helfer angemeldet und werden deshalb auf das schwarze Brett umgeleitet.')
        return redirect("helfen")
    else:
        return HttpResponse("Sie sind nicht angemeldet")

@login_required
def helfen(request):
    if request.user.is_authenticated and request.user.person.group == "H":
        # TODO siehe public blackboard
        return render(request, 'app/app_inneed.html')

    elif request.user.is_authenticated and request.user.person.group == "E":
        messages.add_message(request, messages.INFO,
                             'Sie sind als Einkaufssuchender angemeldet und wurden deshalb auf zu Ihrer Einkaufsliste umgeleitet.')
        return redirect("einkaufsliste")
    else:
        return HttpResponse("Sie sind nicht angemeldet")

def listings(request):
    if request.is_ajax and request.method == "GET":
        location = request.GET.get("location", None)
        status = request.GET.get("status", None)

        if not location is None and not status is None:
            query = Einkaufsauftrag.objects.filter(user__person__location=location, status=status)
            data = serializers.serialize("json", query, status=200)
            data["valid"] = True
            data["status"] = 200

            data["selected_loc´"] = location
            data["selected_status"] = status

            return data

    return JsonResponse({}, status=400)


def helfen_voransicht(request):
    form = SelectionForm
    return render(request, 'public/preview_blackboard.html', {'form': form})

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