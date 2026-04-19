from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import UsuarioForm
from .models import Cita, PerfilUsuario, Tratamiento, Usuario


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        usuario = authenticate(request, username=username, password=password)
        if usuario is None:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'login.html')
        login(request, usuario)
        messages.success(
            request,
            f'Bienvenid@ {usuario.nombre_completo}',
            extra_tags='welcome',
        )
        return redirect('index')
    return render(request, 'login.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('index')


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

        if request.user.is_staff and perfil_usuario:
            if perfil_usuario.rol == 'administrador':
                return redirect('panel_admin')
            elif perfil_usuario.rol == 'profesional':
                return redirect('panel_profesional')

    if request.method == 'POST':
        username = request.POST.get('profesi-username', '').strip()
        password = request.POST.get('profesi-password', '')
        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            messages.error(request, 'Usuario o contrasena incorrectos.')
            return render(request, "profesional.html")

        perfil_usuario = getattr(usuario, 'perfil', None)

        if not usuario.is_staff or not perfil_usuario:
            messages.error(request, 'La cuenta no tiene permisos de acceso interno.')
            return render(request, "profesional.html")
        
        if perfil_usuario.rol not in ['administrador', 'profesional']:
            messages.error(request, 'La cuenta no tiene permisos de administrador ni profesional.')
            return render(request, "profesional.html")

        login(request, usuario)


        if not request.POST.get('profesi-remember-me'):
             request.session.set_expiry(0)

        if perfil_usuario.rol == 'administrador':
            return redirect('panel_admin')

        return redirect('panel_profesional')

    return render(request, "profesional.html")


@login_required
def panel_admin(request):
    perfil_usuario = getattr(request.user, 'perfil', None)

    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'administrador':
        return redirect('profesional')

    profesionales = Usuario.objects.filter(perfil__rol='profesional')

    return render(request, 'panel_admin.html', {
        'profesionales': profesionales
    })

@login_required
def crear_profesional(request):
    perfil_usuario = getattr(request.user, 'perfil', None)

    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'administrador':
        return redirect('profesional')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        email = request.POST.get('email', '').strip()
        celular = request.POST.get('celular', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('panel_admin')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('panel_admin')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('panel_admin')

        perfil_profesional = PerfilUsuario.objects.get(rol='profesional')

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1,
            nombre_completo=nombre_completo,
            celular=celular,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            perfil=perfil_profesional,
            is_staff=True
        )

        messages.success(request, 'Profesional creado correctamente.')
        return redirect('panel_admin')

    return redirect('panel_admin')

@login_required
def editar_profesional(request, id):
    perfil_usuario = getattr(request.user, 'perfil', None)

    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'administrador':
        return redirect('profesional')

    profesional = get_object_or_404(Usuario, id=id, perfil__rol='profesional')

    if request.method == 'POST':
        profesional.username = request.POST.get('username', '').strip()
        profesional.nombre_completo = request.POST.get('nombre_completo', '').strip()
        profesional.email = request.POST.get('email', '').strip()
        profesional.celular = request.POST.get('celular', '').strip()
        profesional.direccion = request.POST.get('direccion', '').strip()
        profesional.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None

        nueva_password = request.POST.get('password', '').strip()
        if nueva_password:
            profesional.set_password(nueva_password)

        profesional.save()
        messages.success(request, 'Profesional actualizado correctamente.')
        return redirect('panel_admin')

    return render(request, 'editar_profesional.html', {
        'profesional': profesional
    })

@login_required
def eliminar_profesional(request, id):
    perfil_usuario = getattr(request.user, 'perfil', None)

    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'administrador':
        return redirect('profesional')

    profesional = get_object_or_404(Usuario, id=id, perfil__rol='profesional')

    if request.method == 'POST':
        profesional.delete()
        messages.success(request, 'Profesional eliminado correctamente.')

    return redirect('panel_admin')


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


@login_required
def vista_cliente_profesi(request):
    perfil_usuario = getattr(request.user, 'perfil', None)
    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'profesional':
        messages.error(request, 'No tienes permiso para acceder a la vista de clientes.')
        return redirect('profesional')

    clientes_db = Usuario.objects.filter(perfil__rol='usuario')

    clientes_tabla = []
    for cliente in clientes_db:
        ultimo_tratamiento = Tratamiento.objects.filter(usuario=cliente).order_by('-fecha').first()

        clientes_tabla.append({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'ultimo_tratamiento': ultimo_tratamiento.nombre if ultimo_tratamiento else 'Sin tratamientos',
            'fecha': ultimo_tratamiento.fecha if ultimo_tratamiento else '',
        })

    return render(request, 'vista_cliente_profesi.html', {
        'nombre_profesional': request.user.nombre_completo,
        'clientes_tabla': clientes_tabla,
    })
