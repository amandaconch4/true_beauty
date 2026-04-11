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
from django.urls import path
from core.views import (
    agendar_view,
    index,
    login_view,
    logout_profesional_view,
    recuperar_password_view,
    recuperar_password_enviado_view,
    profesional_view,
    registro_profesional_view,
    registro,
    servicios_view,
    panel_profesional,
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('servicios/', servicios_view, name='servicios'),
    path('registro/', registro, name='registro'),
    path('registro-profesional/', registro_profesional_view, name='registro_profesional'),
    path('agendar_hora/', agendar_view, name='agendar_hora'),
    path('admin/', admin.site.urls),
    path('profesional/', profesional_view, name='profesional'),
    path('profesional/logout/', logout_profesional_view, name='logout_profesional'),
    path('panel_profesional/', panel_profesional, name='panel_profesional'),
    path('panel-profesional/', panel_profesional),
    path('cambiar-password/', profesional_view, name='cambiar_password'),
    path('recuperar-password/', recuperar_password_view, name='password_reset'),
    path('recuperar_password_enviado.html', recuperar_password_enviado_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='restablecer_confirmar.html'),name='password_reset_confirm'),
    path('reset/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='restablecer_completo.html'), name='password_reset_complete'),
  
]


