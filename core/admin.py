from django.contrib import admin

from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nombre_completo", "celular", "es_profesional", "salon")
    search_fields = ("usuario__username", "nombre_completo", "celular", "salon")
