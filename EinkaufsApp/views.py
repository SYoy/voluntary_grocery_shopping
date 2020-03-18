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

# Queries
from EinkaufsApp.models import Einkaufsauftrag
from django.contrib.auth.models import User

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
        auftraege = Einkaufsauftrag.objects.filter(user_id=request.user.id).order_by("date_added").values()
        most_recent = None

        if auftraege.count() > 0:
            for ob in auftraege:
                if ob["status"] == "aktiv":
                    most_recent = ob
                    break
                elif ob["status"] == "angenommen" and most_recent is None:
                    most_recent = ob
                    break
            if most_recent is None:
                most_recent = auftraege[0]

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
                return render(request, 'app/app_inneed.html', {'form': form, "akt_auftrag": most_recent})
        else:
            form = EinkaufsauftragForm(request.POST)
        return render(request, 'app/app_inneed.html', {'form': form, "akt_auftrag": most_recent})

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
            if location == "ALL":
                query = Einkaufsauftrag.objects.filter(status=status).order_by("date_added")
            else:
                query = Einkaufsauftrag.objects.filter(user__person__location=location, status=status).order_by("date_added")

            users = User.objects.all()
            map = {}
            for user in users:
                map[user.id] = user.person.location

            data = serializers.serialize("json", query)

            return JsonResponse({"data": data, "valid": True,
                                 "map": map,
                                 "selected_loc": location,
                                 "selected_status": status}, status=200, safe=False)

    return JsonResponse({}, status=400)


def helfen_voransicht(request):
    form = SelectionForm
    return render(request, 'public/preview_blackboard.html', {'form': form})

def faq(request):
    return HttpResponse("FAQ Todo")

