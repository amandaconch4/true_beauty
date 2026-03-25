from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

Usuario = get_user_model()


class RegistroForm(UserCreationForm):
    username = forms.CharField(
        max_length=18,
        min_length=5,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="El nombre de usuario debe tener entre 5 y 18 caracteres y no contener espacios.",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        help_text="Ingrese un correo electr\u00f3nico v\u00e1lido.",
    )
    nombre_completo = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Ingrese su nombre completo (m\u00ednimo 8 caracteres).",
    )
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Debe tener al menos 13 a\u00f1os.",
    )
    direccion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Direcci\u00f3n opcional, pero debe tener al menos 5 caracteres si se ingresa.",
    )
    celular = forms.CharField(
        max_length=9,
        min_length=9,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Ingrese un n\u00famero de celular v\u00e1lido de 9 d\u00edgitos.",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "nombre_completo",
            "password1",
            "password2",
            "fecha_nacimiento",
            "direccion",
            "celular",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if " " in username:
            raise ValidationError("El nombre de usuario no puede contener espacios.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo electr\u00f3nico ya est\u00e1 registrado.")
        return email

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get("nombre_completo")
        if len(nombre.strip()) < 8:
            raise ValidationError("El nombre completo debe tener al menos 8 caracteres.")
        return nombre

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get("fecha_nacimiento")
        if fecha:
            hoy = timezone.now().date()
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            if edad < 13:
                raise ValidationError("Debe tener al menos 13 a\u00f1os.")
        return fecha

    def clean_direccion(self):
        direccion = self.cleaned_data.get("direccion")
        if direccion and len(direccion.strip()) < 5:
            raise ValidationError("La direcci\u00f3n debe tener al menos 5 caracteres.")
        return direccion

    def clean_celular(self):
        celular = self.cleaned_data.get("celular")
        if not re.match(r"^\d{9}$", celular):
            raise ValidationError("El n\u00famero de celular debe tener exactamente 9 d\u00edgitos.")
        return celular

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password:
            if len(password) < 6 or len(password) > 18:
                raise ValidationError("La contrase\u00f1a debe tener entre 6 y 18 caracteres.")
            if not re.search(r"[A-Z]", password):
                raise ValidationError("La contrase\u00f1a debe contener al menos una may\u00fascula.")
            if not re.search(r"\d", password):
                raise ValidationError("La contrase\u00f1a debe contener al menos un n\u00famero.")
            if not re.search(r"[.,!@#$%^&*]", password):
                raise ValidationError(
                    "La contrase\u00f1a debe contener al menos un car\u00e1cter especial (.,!@#$%^&*)."
                )
        return password


class RegistroProfesionalForm(RegistroForm):
    salon = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Ingrese el nombre del sal\u00f3n o lugar de trabajo.",
    )
