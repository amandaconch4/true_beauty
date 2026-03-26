from django import forms
from .models import Usuario, PerfilUsuario
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re

from .models import Usuario, PerfilUsuario

# Formulario para crear un Usuario
Usuario = get_user_model()

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre_completo', 'password1', 'fecha_nacimiento', 'direccion', 'celular']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hace los campos obligatorios excepto dirección
        campos_obligatorios = ['username', 'email', 'nombre_completo', 'fecha_nacimiento', 'celular']
        # Si es para editar, la contraseña NO es obligatoria
        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
        else:
            campos_obligatorios.append('password1')
        for field_name, field in self.fields.items():
            if field_name in campos_obligatorios:
                field.required = True
                field.error_messages = {'required': f'El campo {field.label} es obligatorio'}
            else:
                field.required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return username
        qs = Usuario.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")
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
            raise forms.ValidationError("El correo electrónico no puede estar vacío")
        if " " in email:
            raise forms.ValidationError("El correo electrónico no puede contener espacios.")
        import re
        dominio_valido = re.match(r'^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        if not dominio_valido:
            raise forms.ValidationError("El correo electrónico debe tener un dominio válido.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Si se quiere editar y no se ingresa una nueva contraseña, permite dejarlo vacío
        if self.instance and self.instance.pk and not password1:
            return None
        if not password1:
            raise forms.ValidationError("La contraseña no puede estar vacía")
        if len(password1) < 6 or len(password1) > 18:
            raise forms.ValidationError("La contraseña debe tener entre 6 y 18 caracteres.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos una mayúscula.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not any(char in "!@#$%^&*(),." for char in password1):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password1
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular:
            raise forms.ValidationError("El número de celular no puede estar vacío")
        if not re.match(r'^\d{9}$', celular):
            raise forms.ValidationError("El número de celular debe tener exactamente 9 dígitos.")
        return celular

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

        if password:
            user.set_password(password)
        else:
            # Recupera el hash original directamente desde la base de datos
            if user.pk:
                from core.models import Usuario
                original = Usuario.objects.get(pk=user.pk)
                user.password = original.password

        if commit:
            user.save()
        return user
    
# Formulario para crear un perfil de usuario (rol)
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['rol']

