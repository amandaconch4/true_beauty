from django.shortcuts import redirect, render
from .forms import UsuarioForm
from django.contrib import messages
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
            # Asigna el perfil de usuario normal (rol='usuario')
            perfil_usuario = PerfilUsuario.objects.filter(rol='usuario').first()
            if perfil_usuario is None:
                perfil_usuario = PerfilUsuario.objects.create(rol='usuario')
            usuario.perfil = perfil_usuario
            usuario.save()
            messages.success(request, "¡Registro exitoso! Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            # Limpia mensajes anteriores de error
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()
    return render(request, 'registro.html', {
        'usuario_form': usuario_form
    })


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
