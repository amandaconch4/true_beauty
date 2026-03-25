from django.shortcuts import render
from .forms import RegistroForm

def index(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def servicios_view(request):
    return render(request, "servicios.html")

def registro_view(request):
    form = RegistroForm()
    return render(request, "registro.html", {'usuario_form': form})

def agendar_view(request):
    return render(request, "agendar_hora.html")

def profesional_view(request):
    return render(request, "profesional.html")
