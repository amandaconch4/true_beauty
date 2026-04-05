from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UsuarioForm
from .models import PerfilUsuario


def index(request):
    return render(request, "index.html")


def login_view(request):
    return render(request, "login.html")


def servicios_view(request):
    return render(request, "servicios.html")


def registro(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            perfil_usuario, _ = PerfilUsuario.objects.get_or_create(rol='usuario')
            usuario.perfil = perfil_usuario
            usuario.save()
            messages.success(request, "Registro exitoso. Ya puedes iniciar sesion.")
            return redirect('login')

        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()

    return render(request, 'registro.html', {'usuario_form': usuario_form})


def agendar_view(request):
    return render(request, "agendar_hora.html")


def profesional_view(request):
    return render(request, "profesional.html")


def registro_profesional_view(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            perfil_profesional, _ = PerfilUsuario.objects.get_or_create(rol='profesional')
            usuario.perfil = perfil_profesional
            usuario.save()
            messages.success(request, "Registro profesional exitoso. Ya puedes iniciar sesion.")
            return redirect('profesional')

        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()

    return render(request, 'agregar_profesional.html', {'usuario_form': usuario_form})
