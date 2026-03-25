from django.shortcuts import redirect, render

from .forms import RegistroForm, RegistroProfesionalForm


def index(request):
    return render(request, "index.html")


def login_view(request):
    return render(request, "login.html")


def servicios_view(request):
    return render(request, "servicios.html")


def registro_view(request):
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "registro.html", {"usuario_form": form})


def agendar_view(request):
    return render(request, "agendar_hora.html")


def profesional_view(request):
    return render(request, "profesional.html")


def registro_profesional_view(request):
    form = RegistroProfesionalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profesional")
    return render(request, "registro_profesi.html", {"profesional_form": form})
