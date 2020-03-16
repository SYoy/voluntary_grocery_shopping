from django.http import HttpResponse


def start(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def registration(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def einkaufsliste(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def helfen(request):
    return HttpResponse("Hello, world. You're at the polls index.")