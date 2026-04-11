from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import UsuarioForm
from .models import Cita, PerfilUsuario, Tratamiento, Usuario


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
    if request.user.is_authenticated:
        perfil_usuario = getattr(request.user, 'perfil', None)
        if request.user.is_staff and perfil_usuario and perfil_usuario.rol == 'profesional':
            return redirect('panel_profesional')

    if request.method == 'POST':
        username = request.POST.get('profesi-username', '').strip()
        password = request.POST.get('profesi-password', '')
        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            messages.error(request, 'Usuario o contrasena incorrectos.')
            return render(request, "profesional.html")

        perfil_usuario = getattr(usuario, 'perfil', None)
        if not usuario.is_staff or not perfil_usuario or perfil_usuario.rol != 'profesional':
            messages.error(request, 'La cuenta no tiene permisos de profesional.')
            return render(request, "profesional.html")

        login(request, usuario)

        if not request.POST.get('profesi-remember-me'):
            request.session.set_expiry(0)

        return redirect('panel_profesional')

    return render(request, "profesional.html")


def recuperar_password_view(request):
    if request.method == 'POST':
        return redirect('password_reset_done')

    return render(request, 'recuperar_password.html')


@login_required
def logout_profesional_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente.')
    return redirect('profesional')


def recuperar_password_enviado_view(request):
    return render(request, 'recuperar_password_enviado.html')


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

@login_required
def panel_profesional(request):
    # Verificar si el usuario es un profesional
    perfil_usuario = getattr(request.user, 'perfil', None)
    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'profesional':
        messages.error(request, 'No tienes permiso para acceder al panel profesional.')
        return redirect('profesional')  # Redirigir al login de profesional o a otra página

    citas_hoy = Cita.objects.filter(
        profesional=request.user,
        fecha=date.today()
    ).order_by('hora')

    clientes_db = Usuario.objects.filter(perfil__rol='usuario')

    clientes = []
    for cliente in clientes_db:
        ultimo_tratamiento = Tratamiento.objects.filter(usuario=cliente).order_by('-fecha').first()

        clientes.append({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'ultimo_tratamiento': ultimo_tratamiento.nombre if ultimo_tratamiento else 'Sin tratamientos',
            'fecha': ultimo_tratamiento.fecha if ultimo_tratamiento else '',
        })
    


    return render(request, 'panel_profesional.html', {
        'nombre_profesional':request.user.nombre_completo,
        'clientes': clientes,
        'citas_hoy': citas_hoy,
    })
