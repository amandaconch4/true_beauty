from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('profesional', 'Profesional'),
        ('usuario', 'Usuario')
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return self.rol

class Usuario(AbstractUser):
    first_name = None
    last_name = None

    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.CharField(max_length=300, blank=True)
    celular = models.CharField(max_length=9)
    perfil = models.ForeignKey('PerfilUsuario', on_delete=models.CASCADE, related_name='usuarios', null=True)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'nombre_completo', 'fecha_nacimiento', 'celular']
    
    def __str__(self):
        return f"{self.username} ({self.get_nombre_rol()})"
    
    def get_nombre_rol(self):
        return self.perfil.get_rol_display() if self.perfil else 'Sin rol'

class FichaCapilar(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ficha_capilar'
    )

    tipo_cabello = models.CharField(max_length=50)
    estado_cabello = models.TextField()
    tratamientos_previos = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Ficha de {self.usuario.username}"

    def save(self, *args, **kwargs):
        if not self.usuario.perfil or self.usuario.perfil.rol != 'usuario':
            raise ValidationError("Solo los clientes pueden tener ficha capilar")
        super().save(*args, **kwargs)
    
class Tratamiento(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tratamientos'
    )

    profesional = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tratamientos_realizados'
    )

    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre
    
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Usuario,on_delete=models.CASCADE,related_name='citas_cliente')

    profesional = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='citas_profesional'
    )

    servicio = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"{self.cliente.nombre_completo} - {self.fecha} {self.hora}"