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
from django.utils import timezone


## PUBLIC
def start(request):
    query = User.objects.filter(person__group="H")
    return render(request, 'public/start.html', {"helfer_count": len(query)})


## PUBLIC
def impressum(request):
    return render(request, 'public/impressum.html')


## PUBLIC
def datenschutz(request):
    return render(request, 'public/datenschutz.html')


## PUBLIC
def faq(request):
    return render(request, 'public/faq.html')


## PUBLIC - BLACKBOARD
def helfen_voransicht(request):
    form = SelectionForm
    return render(request, 'public/preview_blackboard.html', {'form': form})


## PUBLIC - BLACKBOARD
def listings(request):
    if request.is_ajax and request.method == "GET":
        location = request.GET.get("location", None)
        status = request.GET.get("status", None)

        if not location is None and not status is None:
            if location == "ALL":
                # TODO mischen?
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


## PUBLIC
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


## PUBLIC
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


## HOME
@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html', {'group': request.user.person.group, 'username': request.user.username})
    else:
        return HttpResponse("Sie sind nicht angemeldet")


## EMPFAENGER
@login_required
def einkaufsliste(request):
    if request.user.is_authenticated and request.user.person.group in ["E", "D", "S"]:
        if request.method == 'POST':
            form = EinkaufsauftragForm(request.POST)
            if form.is_valid():
                # TODO check other active listings -> remove
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
                return redirect("einkaufsliste")
        else:
            form = EinkaufsauftragForm()

        auftraege = Einkaufsauftrag.objects.filter(user_id=request.user.id).order_by("-date_added").values()
        most_recent = None

        # TODO - refactor
        if auftraege.count() > 0:
            for ob in auftraege:
                if ob["status"] == "aktiv":
                    most_recent = ob
                    break
                elif ob["status"] == "angenommen" and most_recent is None:
                    most_recent = ob
                    break
            if most_recent is None:
                for ob in auftraege:
                    if ob["status"] == "abgeschlossen":
                        most_recent = ob
                        break
                if most_recent is None:
                    for ob in auftraege:
                        if ob["status"] == "inaktiv":
                            most_recent = ob
                            break

        return render(request, 'app/app_inneed.html', {'form': form, "akt_auftrag": most_recent})

    elif request.user.is_authenticated and request.user.person.group == "H":
        messages.add_message(request, messages.INFO, 'Sie sind als Helfer angemeldet und werden deshalb auf das schwarze Brett umgeleitet.')
        return redirect("helfen")
    else:
        return redirect("start")


## EMPFAENGER
@login_required
def setInactive(request):
    if request.user.is_authenticated and request.is_ajax and request.method == "POST":
        ID_auftrag = request.POST.get("id_listing", None)
        ID_user = request.POST.get("user_id", None)
        auftrag = Einkaufsauftrag.objects.filter(id=ID_auftrag, user_id=ID_user)

        if int(ID_user) == request.user.id and len(auftrag) == 1:
            auftrag.update(status="inaktiv", date_done=timezone.now())

            return JsonResponse({"valid": True}, status=200)
        else:
            return JsonResponse({"valid": False}, status=400)


## EMPFAENGER
@login_required
def setDone(request):
    if request.user.is_authenticated and request.is_ajax and request.method == "POST":
        ID_auftrag = request.POST.get("id_listing", None)
        ID_user = request.POST.get("user_id", None)
        auftrag = Einkaufsauftrag.objects.filter(id=ID_auftrag, user_id=ID_user)


        if int(ID_user) == request.user.id and len(auftrag) == 1:
            auftrag.update(status="abgeschlossen", date_done=timezone.now())

            return JsonResponse({"valid": True}, status=200)
        else:
            return JsonResponse({"valid": False}, status=400)


## HELFER
@login_required
def helfen(request):
    form = SelectionForm
    return render(request, 'app/app_helper.html', {'form': form})


## HELFER
@login_required
def helfer_einkaufslisten(request):
    return render(request, 'app/inWork.html', {'group': request.user.person.group, 'username': request.user.username})


## HELFER
@login_required
def setInWork(request):
    if request.user.is_authenticated and request.user.person.group in ["H", "S"]:
        if request.is_ajax and request.method == "POST":
            auftrag_id = request.POST.get("id_listing", None)
            auftrag = Einkaufsauftrag.objects.filter(id=int(auftrag_id), status="aktiv")

            if len(auftrag) == 1:
                auftrag.update(status="angenommen", working_on_user_id=request.user.id)

                return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)

## HELFER
@login_required
def getAccepted(request):
    if request.user.is_authenticated and request.user.person.group in ["H", "S"]:
        if request.is_ajax and request.method == "GET":
            user_id = request.user.id
            query_ang = Einkaufsauftrag.objects.filter(working_on_user_id=user_id, status="angenommen").order_by("-date_added")
            query_closed = Einkaufsauftrag.objects.filter(working_on_user_id=user_id, status="abgeschlossen").order_by("date_added")

            users = User.objects.all()
            map = {}
            for user in users:
                map[user.id] = user.person.location

            data_ang = serializers.serialize("json", query_ang)
            data_closed = serializers.serialize("json", query_closed)

            return JsonResponse({"data_a": data_ang, "data_closed": data_closed,
                                 "valid": True, "map": map}, status=200, safe=False)

        return JsonResponse({}, status=400)
    else:
        return redirect("home")