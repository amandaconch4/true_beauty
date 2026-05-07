from django.conf import settings
from django.core.mail import send_mail
from django.utils.formats import date_format, time_format


def enviar_recordatorio_cita(cita):
    """Envia por email el recordatorio de una cita pendiente."""
    if not cita.cliente.email:
        return 0

    fecha = date_format(cita.fecha, 'l d \\d\\e F \\d\\e Y', use_l10n=True)
    hora = time_format(cita.hora, 'H:i')
    profesional = cita.profesional.nombre_completo or cita.profesional.username

    asunto = 'Recordatorio de tu cita en True Beauty'
    mensaje = (
        f'Hola {cita.cliente.nombre_completo},\n\n'
        f'Te recordamos que tienes una cita en True Beauty el {fecha} a las {hora}.\n'
        f'Servicio: {cita.servicio}\n'
        f'Profesional: {profesional}\n\n'
        'Te esperamos.\n\n'
        'True Beauty'
    )

    return send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [cita.cliente.email],
        fail_silently=False,
    )
