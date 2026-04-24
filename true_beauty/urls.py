"""
URL configuration for true_beauty project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from core import views
from core.views import (
    agendar_view,
    index,
    login_view,
    logout_profesional_view,
    logout_view,
    profesional_view,
    registro_profesional_view,
    registro,
    servicios_view,
    panel_profesional,
    panel_admin,
    crear_profesional,
    editar_profesional,
    eliminar_profesional,
    eliminar_cuenta,
    cancelar_cita,
    mis_citas,
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout-profesional/', logout_profesional_view, name='logout_profesional'),
    path('servicios/', servicios_view, name='servicios'),
    path('registro/', registro, name='registro'),
    path('registro-profesional/', registro_profesional_view, name='registro_profesional'),
    path('agendar_hora/', agendar_view, name='agendar_hora'),
    path('admin/', admin.site.urls),
    path('perfil/', views.perfil, name='perfil'),
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta'),
    path('cancelar-cita/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),
    path('mis-citas/', mis_citas, name='mis_citas'),
    path('panel_admin/', panel_admin, name='panel_admin'),
    path('crear-profesional/', crear_profesional, name='crear_profesional'),
    path('editar-profesional/<int:id>/', editar_profesional, name='editar_profesional'),
    path('eliminar-profesional/<int:id>/', eliminar_profesional, name='eliminar_profesional'),

    path('profesional/', profesional_view, name='profesional'),
    path('panel_profesional/', panel_profesional, name='panel_profesional'),
    path('panel-profesional/', panel_profesional, name='panel_profesional_alt'),
    
    path('cambiar-password/', profesional_view, name='cambiar_password'),
     path(
        'recuperar-password/',
        auth_views.PasswordResetView.as_view(
            template_name='recuperar_password.html',
            email_template_name='emails/password_reset_email.html',
            subject_template_name='emails/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset'
    ),
    path(
        'recuperar-password/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='recuperar_password_enviado.html'
        ),
        name='password_reset_done'
    ),
    #path('recuperar-password/',auth_views.PasswordResetView.as_view(template_name='recuperar_password.html'),name='password_reset'),
    #path('recuperar-password/enviado/',auth_views.PasswordResetDoneView.as_view(template_name='recuperar_password_enviado.html'),name='password_reset_done'),
    #path('recuperar-password-enviado/',auth_views.PasswordResetDoneView.as_view(template_name='recuperar_password_enviado.html'),name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='restablecer_confirmar.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),

    path(
        'reset/completo/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='restablecer_completo.html',
        ),
        name='password_reset_complete',
    ),
    path('clientes-profesional/', views.vista_cliente_profesi, name='vista_cliente_profesi'),
    path('cliente/<int:id>/ficha/', views.ficha_capilar, name='ficha_capilar'),
    path('cliente/<int:id>/cuidados/', views.cuidados_cliente, name='cuidados_cliente'),
    path('cliente/<int:id>/historial/', views.historial_cliente, name='historial_cliente'),
    path('cliente/<int:id>/reservas/', views.reservas_cliente, name='reservas_cliente'),
  
]


