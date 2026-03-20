from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def servicios_view(request):
    return render(request, "servicios.html")

def registro_view(request):
    return render(request, "registro.html")
