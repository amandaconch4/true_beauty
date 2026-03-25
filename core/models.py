from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    nombre_completo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=9)
    salon = models.CharField(max_length=120, blank=True)
    es_profesional = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

