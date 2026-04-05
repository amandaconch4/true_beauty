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
from django.urls import path
from core.views import (
    agendar_view,
    index,
    login_view,
    profesional_view,
    registro_profesional_view,
    registro,
    servicios_view,
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
    path('panel-profesional/', profesional_view, name='panel_profesional'),
]

