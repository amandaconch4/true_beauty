from django.contrib import admin
from .models import PerfilUsuario, Usuario, TipoProducto, Producto


admin.site.register(Usuario)
admin.site.register(PerfilUsuario)
admin.site.register(TipoProducto)
admin.site.register(Producto)
