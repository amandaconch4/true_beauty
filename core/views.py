import re
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import UsuarioForm
from .models import Cita, CuidadoRecomendacion, PerfilUsuario, Tratamiento, Usuario, FichaCapilar


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
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            perfil_usuario, _ = PerfilUsuario.objects.get_or_create(rol='usuario')
            usuario.perfil = perfil_usuario
            usuario.save()
            messages.success(request, "Registro exitoso. Ya puedes iniciar sesion.")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('login')

        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "Error en el formulario. Por favor, revisa los datos.")
    else:
        usuario_form = UsuarioForm()

    return render(request, 'registro.html', {
        'usuario_form': usuario_form,
        'next_url': next_url,
    })


@login_required(login_url='/login/')
def agendar_view(request):
    perfil_usuario = getattr(request.user, 'perfil', None)
    desde_panel_profesional = (
        request.GET.get('desde') == 'panel_profesional'
        and request.user.is_authenticated
        and request.user.is_staff
        and perfil_usuario
        and perfil_usuario.rol == 'profesional'
    )

    # Obtener citas del usuario actual
    mis_citas = Cita.objects.none() if desde_panel_profesional else Cita.objects.filter(
        cliente=request.user
    ).order_by('fecha', 'hora')
    
    if request.method == 'POST':
        servicio = request.POST.get('servicio', '').strip()
        fecha_str = request.POST.get('fecha', '').strip()
        hora_str = request.POST.get('hora', '').strip()
        cliente_id = request.POST.get('cliente_id', '').strip()
        profesional_id = request.POST.get('profesional_id', '').strip()
        
        # Validaciones
        errores = []
        cliente_asignado = request.user
        profesional_asignado = None

        if desde_panel_profesional:
            if not cliente_id:
                errores.append('Debes seleccionar un cliente.')
            else:
                cliente_asignado = Usuario.objects.filter(id=cliente_id, perfil__rol='usuario').first()
                if cliente_asignado is None:
                    errores.append('El cliente seleccionado no existe.')

            if not profesional_id:
                errores.append('Debes seleccionar un profesional.')
            else:
                profesional_asignado = Usuario.objects.filter(id=profesional_id, perfil__rol='profesional').first()
                if profesional_asignado is None:
                    errores.append('El profesional seleccionado no existe.')
        
        if not servicio:
            errores.append('Debes seleccionar un servicio.')
        
        if not fecha_str:
            errores.append('Debes seleccionar una fecha.')
        
        if not hora_str:
            errores.append('Debes seleccionar una hora.')
        
        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, "agendar_hora.html", {
                'mis_citas': mis_citas,
                'desde_panel_profesional': desde_panel_profesional,
                'clientes': Usuario.objects.filter(perfil__rol='usuario', is_active=True).order_by('nombre_completo'),
                'profesionales': Usuario.objects.filter(perfil__rol='profesional', is_active=True).order_by('nombre_completo'),
                'cliente_seleccionado_id': cliente_id,
                'profesional_seleccionado_id': profesional_id,
                'servicio_seleccionado': servicio,
                'fecha_seleccionada': fecha_str,
                'hora_seleccionada': hora_str,
            })
        
        # Buscar un profesional disponible (que no tenga cita a esa hora)
        from datetime import datetime, time
        
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()
        
        # Obtener profesionales
        profesionales = Usuario.objects.filter(
            perfil__rol='profesional'
        )
        
        # Verificar si hay profesionales en el sistema
        if not profesionales.exists():
            messages.error(request, 'No hay profesionales configurados en el sistema. Contacta al administrador.')
            return render(request, "agendar_hora.html", {
                'mis_citas': mis_citas,
                'desde_panel_profesional': desde_panel_profesional,
                'clientes': Usuario.objects.filter(perfil__rol='usuario', is_active=True).order_by('nombre_completo'),
                'profesionales': profesionales,
                'cliente_seleccionado_id': cliente_id,
                'profesional_seleccionado_id': profesional_id,
                'servicio_seleccionado': servicio,
                'fecha_seleccionada': fecha_str,
                'hora_seleccionada': hora_str,
            })
        
        if desde_panel_profesional:
            cita_existente = Cita.objects.filter(
                profesional=profesional_asignado,
                fecha=fecha,
                hora=hora,
                estado__in=['pendiente', 'realizada']
            ).first()

            if cita_existente:
                profesional_asignado = None
        else:
            profesional_asignado = None
            for profesional in profesionales:
                # Verificar si el profesional ya tiene una cita a esa hora
                cita_existente = Cita.objects.filter(
                    profesional=profesional,
                    fecha=fecha,
                    hora=hora,
                    estado__in=['pendiente', 'realizada']
                ).first()
                
                if not cita_existente:
                    profesional_asignado = profesional
                    break
        
        if not profesional_asignado:
            if desde_panel_profesional:
                messages.error(request, f'El profesional seleccionado no esta disponible el {fecha_str} a las {hora_str}.')
            else:
                messages.error(request, f'No hay profesionales disponibles el {fecha_str} a las {hora_str}. Todos los profesionales tienen citas agendadas en ese horario. Por favor, selecciona otra fecha u hora.')
            return render(request, "agendar_hora.html", {
                'mis_citas': mis_citas,
                'desde_panel_profesional': desde_panel_profesional,
                'clientes': Usuario.objects.filter(perfil__rol='usuario', is_active=True).order_by('nombre_completo'),
                'profesionales': profesionales,
                'cliente_seleccionado_id': cliente_id,
                'profesional_seleccionado_id': profesional_id,
                'servicio_seleccionado': servicio,
                'fecha_seleccionada': fecha_str,
                'hora_seleccionada': hora_str,
            })
        
        # Crear la cita
        nombres_servicios = {
            'corte': 'Corte de pelo',
            'alisado': 'Alisado',
            'botox': 'Botox capilar',
            'peinado': 'Peinado',
            'keratina': 'Tratamiento de keratina',
            'coloracion': 'Coloración',
        }
        
        cita = Cita.objects.create(
            cliente=cliente_asignado,
            profesional=profesional_asignado,
            servicio=nombres_servicios.get(servicio, servicio),
            fecha=fecha,
            hora=hora,
            estado='pendiente'
        )
        
        messages.success(request, f'¡Cita agendada exitosamente! Te esperamos el {fecha_str} a las {hora_str}.')
        
        # Actualizar la lista de citas
        mis_citas = Cita.objects.filter(
            cliente=request.user
        ).order_by('fecha', 'hora')
    
    perfil_usuario = getattr(request.user, 'perfil', None)
    desde_panel_profesional = (
        request.GET.get('desde') == 'panel_profesional'
        and request.user.is_authenticated
        and request.user.is_staff
        and perfil_usuario
        and perfil_usuario.rol == 'profesional'
    )
    profesionales = Usuario.objects.filter(
        perfil__rol='profesional',
        is_active=True,
    ).order_by('nombre_completo')
    clientes = Usuario.objects.filter(
        perfil__rol='usuario',
        is_active=True,
    ).order_by('nombre_completo')

    return render(request, "agendar_hora.html", {
        'mis_citas': mis_citas,
        'desde_panel_profesional': desde_panel_profesional,
        'profesionales': profesionales,
        'clientes': clientes,
    })


def profesional_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.user.is_authenticated:
        perfil_usuario = getattr(request.user, 'perfil', None)
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

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
            return render(request, "profesional.html", {'next_url': next_url})

        perfil_usuario = getattr(usuario, 'perfil', None)

        if not usuario.is_staff or not perfil_usuario:
            messages.error(request, 'La cuenta no tiene permisos de acceso interno.')
            return render(request, "profesional.html", {'next_url': next_url})
        
        if perfil_usuario.rol not in ['administrador', 'profesional']:
            messages.error(request, 'La cuenta no tiene permisos de administrador ni profesional.')
            return render(request, "profesional.html", {'next_url': next_url})

        login(request, usuario)


        if not request.POST.get('profesi-remember-me'):
             request.session.set_expiry(0)

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        if perfil_usuario.rol == 'administrador':
            return redirect('panel_admin')

        return redirect('panel_profesional')

    return render(request, "profesional.html", {'next_url': next_url})


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
        usuario_form = UsuarioForm(request.POST)

        if usuario_form.is_valid():
            perfil_profesional, _ = PerfilUsuario.objects.get_or_create(rol='profesional')
            usuario = usuario_form.save(commit=False)
            usuario.perfil = perfil_profesional
            usuario.is_staff = True
            usuario.save()

            messages.success(request, 'Profesional creado correctamente.')
            return redirect('panel_admin')

        for field_errors in usuario_form.errors.values():
            for error in field_errors:
                messages.error(request, error)
        return redirect('panel_admin')

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

    hoy = date.today()
    inicio_semana = hoy
    fin_semana = hoy + timedelta(days=6)
    citas_semana = Cita.objects.select_related('cliente').filter(
        profesional=request.user,
        fecha__range=(inicio_semana, fin_semana)
    ).order_by('fecha', 'hora')
    citas_por_fecha = {}
    for cita in citas_semana:
        citas_por_fecha.setdefault(cita.fecha, []).append(cita)

    nombres_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    agenda_semana = [
        {
            'nombre': nombres_dias[(inicio_semana + timedelta(days=indice)).weekday()],
            'fecha': inicio_semana + timedelta(days=indice),
            'citas': citas_por_fecha.get(inicio_semana + timedelta(days=indice), []),
            'es_hoy': inicio_semana + timedelta(days=indice) == hoy,
        }
        for indice in range(7)
    ]

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
        'agenda_semana': agenda_semana,
        'hay_citas_semana': citas_semana.exists(),
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
    })

@login_required
def vista_cliente_profesi(request):
    perfil_usuario = getattr(request.user, 'perfil', None)
    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'profesional':
        messages.error(request, 'No tienes permiso para acceder a la vista de clientes.')
        return redirect('profesional')

    query = request.GET.get('q', '').strip()

    clientes = Usuario.objects.filter(perfil__rol='usuario').order_by('nombre_completo')

    if query:
        clientes = clientes.filter(nombre_completo__icontains=query)

    clientes_tabla = []
    for cliente in clientes:
        ultimo_tratamiento = Tratamiento.objects.filter(usuario=cliente).order_by('-fecha').first()

        clientes_tabla.append({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'ultimo_tratamiento': ultimo_tratamiento.nombre if ultimo_tratamiento else 'Sin tratamiento',
            'fecha': ultimo_tratamiento.fecha if ultimo_tratamiento else None,
        })

    cliente_detalle = clientes.first() if clientes.exists() else None

    context = {
        'nombre_profesional': request.user.nombre_completo,
        'clientes_tabla': clientes_tabla,
        'cliente_detalle': cliente_detalle,
        'query': query,
    }

    return render(request, 'vista_cliente_profesi.html', context)

def ficha_capilar(request, id):
    cliente = get_object_or_404(Usuario, id=id)
    ficha = getattr(cliente, 'ficha_capilar', None)

    if request.method == 'POST':
        diagnostico_general = {
            f'general_{numero}': request.POST.get(f'general_{numero}', '')
            for numero in range(1, 6)
        }
        historial = {
            'opciones': request.POST.getlist('historial'),
            'color_original': request.POST.get('color_original', '').strip()[:50],
            'nota': request.POST.get('historial_nota_1', '').strip(),
            'fecha_1': request.POST.get('fecha_historial_1', ''),
        }

        ficha, _ = FichaCapilar.objects.get_or_create(
            usuario=cliente,
            defaults={
                'tipo_cabello': request.POST.get('tipo_cabello', '').strip() or 'Sin especificar',
                'estado_cabello': request.POST.get('estado_cabello', '').strip() or 'Sin diagnostico',
                'tratamientos_previos': request.POST.get('tratamientos_previos', '').strip(),
                'observaciones': request.POST.get('observaciones', '').strip(),
                'diagnostico_general': diagnostico_general,
                'historial': historial,
                'grosor': request.POST.get('grosor', '').strip(),
                'elasticidad': request.POST.get('elasticidad', '').strip(),
                'porosidad': request.POST.get('porosidad', '').strip(),
                'cuero_cabelludo': request.POST.get('cuero_cabelludo', '').strip(),
                'textura': request.POST.get('textura', '').strip(),
                'marca_shampoo': request.POST.get('marca_shampoo', '').strip()[:50],
                'duracion_aproximada': request.POST.get('duracion_aproximada', '').strip(),
            }
        )

        if not _:
            ficha.tipo_cabello = request.POST.get('tipo_cabello', '').strip() or 'Sin especificar'
            ficha.estado_cabello = request.POST.get('estado_cabello', '').strip() or 'Sin diagnostico'
            ficha.tratamientos_previos = request.POST.get('tratamientos_previos', '').strip()
            ficha.observaciones = request.POST.get('observaciones', '').strip()
            ficha.diagnostico_general = diagnostico_general
            ficha.historial = historial
            ficha.grosor = request.POST.get('grosor', '').strip()
            ficha.elasticidad = request.POST.get('elasticidad', '').strip()
            ficha.porosidad = request.POST.get('porosidad', '').strip()
            ficha.cuero_cabelludo = request.POST.get('cuero_cabelludo', '').strip()
            ficha.textura = request.POST.get('textura', '').strip()
            ficha.marca_shampoo = request.POST.get('marca_shampoo', '').strip()[:50]
            ficha.duracion_aproximada = request.POST.get('duracion_aproximada', '').strip()

        ficha.save()

        messages.success(request, 'Ficha capilar guardada correctamente.')
        return redirect('ficha_capilar', id=cliente.id)

    return render(request, 'ficha_capilar.html', {
        'cliente': cliente,
        'ficha': ficha,
        'diagnostico_general': ficha.diagnostico_general if ficha else {},
        'historial': ficha.historial if ficha else {},
    })


def historial_cliente(request, id):
    cliente = get_object_or_404(Usuario, id=id)
    tratamientos = cliente.cuidados_recomendaciones.all()

    return render(request, 'historial.html', {
        'cliente': cliente,
        'tratamientos': tratamientos
    })


def reservas_cliente(request, id):
    perfil_usuario = getattr(request.user, 'perfil', None)
    if not request.user.is_staff or not perfil_usuario or perfil_usuario.rol != 'profesional':
        messages.error(request, 'No tienes permiso para acceder a las reservas profesionales.')
        return redirect('profesional')

    cliente = get_object_or_404(Usuario, id=id, perfil__rol='usuario')
    reservas = Cita.objects.select_related(
        'cliente',
        'profesional',
    ).filter(
        cliente=cliente
    ).order_by('-fecha', '-hora')

    return render(request, 'reservas.html', {
        'nombre_profesional': request.user.nombre_completo,
        'cliente': cliente,
        'reservas': reservas,
    })


def cuidados_cliente(request, id):
    cliente = get_object_or_404(Usuario, id=id)
    cuidados_lista = CuidadoRecomendacion.objects.filter(cliente=cliente)

    if request.method == 'POST':
        cuidado_id = request.POST.get('cuidado_id')

        if cuidado_id:
            cuidado = get_object_or_404(CuidadoRecomendacion, id=cuidado_id, cliente=cliente)
        else:
            cuidado = CuidadoRecomendacion(cliente=cliente)

        cuidado.fecha = request.POST.get('fecha') or None
        cuidado.recomendacion_casa = request.POST.get('recomendacion_casa', '').strip()
        cuidado.producto_recomendado = request.POST.get('producto_recomendado', '').strip()
        cuidado.modo_uso = request.POST.get('modo_uso', '').strip()
        cuidado.frecuencia = request.POST.get('frecuencia', '').strip()
        cuidado.fecha_inicio = request.POST.get('fecha_inicio') or None
        cuidado.fecha_termino = request.POST.get('fecha_termino') or None
        cuidado.save()

        messages.success(request, 'Cuidados y recomendaciones guardados correctamente.')
        return redirect('cuidados_cliente', id=cliente.id)

    cuidado_id = request.GET.get('cuidado_id')
    cuidado = None

    if cuidado_id:
        cuidado = get_object_or_404(CuidadoRecomendacion, id=cuidado_id, cliente=cliente)
    else:
        cuidado = cuidados_lista.first()

    cuidados_form = {
        'id': cuidado.id if cuidado else '',
        'fecha': cuidado.fecha.isoformat() if cuidado and cuidado.fecha else '',
        'recomendacion_casa': cuidado.recomendacion_casa if cuidado else '',
        'producto_recomendado': cuidado.producto_recomendado if cuidado else '',
        'modo_uso': cuidado.modo_uso if cuidado else '',
        'frecuencia': cuidado.frecuencia if cuidado else '',
        'fecha_inicio': cuidado.fecha_inicio.isoformat() if cuidado and cuidado.fecha_inicio else '',
        'fecha_termino': cuidado.fecha_termino.isoformat() if cuidado and cuidado.fecha_termino else '',
    }

    return render(request, 'cuidados_recomendaciones.html', {
        'cliente': cliente,
        'cuidados_lista': cuidados_lista,
        'cuidados_form': cuidados_form,
        'hay_tratamiento': cuidado is not None,
    })

@login_required
def perfil(request):
    usuario = request.user
    
    if request.method == 'POST':
        # Actualizar campos permitidos (excepto fecha_nacimiento)
        usuario.nombre_completo = request.POST.get('nombre_completo', '').strip()
        usuario.email = request.POST.get('email', '').strip()
        usuario.direccion = request.POST.get('direccion', '').strip()
        usuario.celular = request.POST.get('celular', '').strip()
        
        # Validar campos requeridos
        errores = []
        if not usuario.nombre_completo or len(usuario.nombre_completo) < 8:
            errores.append('El nombre completo debe tener al menos 8 caracteres.')
        if not usuario.email:
            errores.append('El correo electrónico es obligatorio.')
        elif ' ' in usuario.email:
            errores.append('El correo electrónico no puede contener espacios.')
        elif not re.match(r'^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', usuario.email):
            errores.append('El correo electrónico debe tener un formato válido.')
        
        # Verificar email único
        if Usuario.objects.filter(email=usuario.email).exclude(pk=usuario.pk).exists():
            errores.append('El correo electrónico ya está en uso.')
        
        # Validar celular
        if not usuario.celular:
            errores.append('El número de celular es obligatorio.')
        elif not re.match(r'^\d{9}$', usuario.celular):
            errores.append('El número de celular debe tener exactamente 9 dígitos.')
        
        # Manejar cambio de contraseña (opcional)
        password_actual = request.POST.get('password_actual', '').strip()
        password_nueva = request.POST.get('password_nueva', '').strip()
        password_confirmar = request.POST.get('password_confirmar', '').strip()
        
        if password_nueva or password_confirmar or password_actual:
            if not password_actual:
                errores.append('Debe ingresar su contraseña actual para cambiarla.')
            elif not usuario.check_password(password_actual):
                errores.append('La contraseña actual es incorrecta.')
            elif password_nueva != password_confirmar:
                errores.append('Las contraseñas nuevas no coinciden.')
            elif len(password_nueva) < 6 or len(password_nueva) > 18:
                errores.append('La contraseña nueva debe tener entre 6 y 18 caracteres.')
            elif not any(char.isupper() for char in password_nueva):
                errores.append('La contraseña nueva debe contener al menos una mayúscula.')
            elif not any(char.isdigit() for char in password_nueva):
                errores.append('La contraseña nueva debe contener al menos un número.')
            elif not any(char in "!@#$%^&*,." for char in password_nueva):
                errores.append('La contraseña nueva debe contener al menos un carácter especial.')
        
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # Guardar cambios
            if password_nueva:
                usuario.set_password(password_nueva)
            usuario.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    
    return render(request, 'mi_perfil.html', {
        'usuario': usuario
    })


@login_required
@require_POST
def eliminar_cuenta(request):
    usuario = request.user
    username = usuario.username
    
    # No permitir eliminar cuentas de administrador o profesional desde aquí
    perfil_usuario = getattr(usuario, 'perfil', None)
    if perfil_usuario and perfil_usuario.rol in ['administrador', 'profesional']:
        messages.error(request, 'No puedes eliminar una cuenta de administrador o profesional desde esta página.')
        return redirect('perfil')
    
    # Cerrar sesión antes de eliminar
    logout(request)
    
    # Eliminar el usuario
    usuario.delete()
    
    messages.success(request, f'Tu cuenta ({username}) ha sido eliminada permanentemente.')
    return redirect('index')


@login_required
@require_POST
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user)
    
    if cita.estado != 'pendiente':
        messages.error(request, 'Solo puedes cancelar citas pendientes.')
        return redirect('agendar_hora')
    
    cita.estado = 'cancelada'
    cita.save()
    
    messages.success(request, f'Tu cita del {cita.fecha} a las {cita.hora} ha sido cancelada.')
    return redirect('agendar_hora')


@login_required(login_url='/login/')
def mis_citas(request):
    citas = Cita.objects.filter(
        cliente=request.user
    ).order_by('fecha', 'hora')
    
    return render(request, 'mis_citas.html', {
        'citas': citas
    })
