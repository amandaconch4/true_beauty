import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import PerfilUsuario


Usuario = get_user_model()


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'nombre_completo',
            'password1',
            'password2',
            'fecha_nacimiento',
            'direccion',
            'celular',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        campos_obligatorios = ['username', 'email', 'nombre_completo', 'fecha_nacimiento', 'celular']

        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
        else:
            campos_obligatorios.extend(['password1', 'password2'])

        for field_name, field in self.fields.items():
            field.required = field_name in campos_obligatorios
            if field.required:
                field.error_messages = {'required': f'El campo {field.label} es obligatorio'}

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username

        qs = Usuario.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("El nombre de usuario ya esta en uso.")
        return username

    def clean_nombre_completo(self):
        nombre_completo = self.cleaned_data.get('nombre_completo')
        if not nombre_completo:
            return nombre_completo
        if len(nombre_completo.strip()) < 8:
            raise forms.ValidationError("El nombre completo debe tener al menos 8 caracteres.")
        return nombre_completo

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El correo electronico no puede estar vacio.")
        if " " in email:
            raise forms.ValidationError("El correo electronico no puede contener espacios.")
        if not re.match(r'^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("El correo electronico debe tener un dominio valido.")

        qs = Usuario.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("El correo electronico ya esta en uso.")

        return email.lower()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if self.instance and self.instance.pk and not password1:
            return None
        if not password1:
            raise forms.ValidationError("La contrasena no puede estar vacia.")
        if len(password1) < 6 or len(password1) > 18:
            raise forms.ValidationError("La contrasena debe tener entre 6 y 18 caracteres.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("La contrasena debe contener al menos una mayuscula.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("La contrasena debe contener al menos un numero.")
        if not any(char in "!@#$%^&*(),." for char in password1):
            raise forms.ValidationError("La contrasena debe contener al menos un caracter especial.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if self.instance and self.instance.pk and not password1 and not password2:
            return None
        if password1 != password2:
            raise forms.ValidationError("Las contrasenas no coinciden.")
        return password2

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular:
            raise forms.ValidationError("El numero de celular no puede estar vacio.")
        if not re.match(r'^\d{9}$', celular):
            raise forms.ValidationError("El numero de celular debe tener exactamente 9 digitos.")
        return celular

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)
        elif user.pk:
            original = Usuario.objects.get(pk=user.pk)
            user.password = original.password

        if commit:
            user.save()
        return user


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']
