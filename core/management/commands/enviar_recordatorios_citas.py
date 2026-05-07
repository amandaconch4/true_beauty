from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.emails import enviar_recordatorio_cita
from core.models import Cita


class Command(BaseCommand):
    help = 'Envia recordatorios por email para citas pendientes proximas.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--horas',
            type=int,
            default=24,
            help='Cantidad de horas hacia adelante para buscar citas. Por defecto: 24.',
        )

    def handle(self, *args, **options):
        horas = options['horas']
        ahora = timezone.localtime()
        limite = ahora + timedelta(hours=horas)

        citas = Cita.objects.select_related('cliente', 'profesional').filter(
            estado='pendiente',
            notificacion_enviada=False,
            fecha__gte=ahora.date(),
            fecha__lte=limite.date(),
        ).order_by('fecha', 'hora')

        enviadas = 0
        omitidas = 0

        for cita in citas:
            fecha_hora = timezone.make_aware(
                datetime.combine(cita.fecha, cita.hora),
                timezone.get_current_timezone(),
            )

            if fecha_hora < ahora or fecha_hora > limite:
                continue

            if not cita.cliente.email:
                omitidas += 1
                self.stdout.write(
                    self.style.WARNING(f'Cita {cita.id} omitida: cliente sin email.')
                )
                continue

            enviar_recordatorio_cita(cita)
            cita.notificacion_enviada = True
            cita.save(update_fields=['notificacion_enviada'])
            enviadas += 1
            self.stdout.write(self.style.SUCCESS(f'Recordatorio enviado para cita {cita.id}.'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Proceso terminado. Enviadas: {enviadas}. Omitidas: {omitidas}.'
            )
        )
