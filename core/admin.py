from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PerfilUsuario, Producto, Servicio, TipoProducto, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'nombre_completo', 'perfil', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informacion adicional', {'fields': ('nombre_completo', 'fecha_nacimiento', 'direccion', 'celular', 'perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informacion adicional', {'fields': ('email', 'nombre_completo', 'fecha_nacimiento', 'direccion', 'celular', 'perfil')}),
    )


admin.site.register(PerfilUsuario)
admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(Servicio)
