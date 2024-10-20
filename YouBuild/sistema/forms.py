from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UsuarioDB,MunicipioDB


class LoginForm(AuthenticationForm):
    pass

class RegistroUsuarioForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    municipio_fk = forms.ModelChoiceField(queryset=MunicipioDB.objects.all(), required=True, label="Municipio")  # Campo Municipio
    direccion = forms.CharField(max_length=255, required=True)  # Campo Dirección
    imagen_perfil = forms.ImageField(required=False)  # Campo Imagen de Perfil

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'fecha_nacimiento', 'municipio_fk', 'direccion', 'imagen_perfil']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear perfil de usuario
            perfil = UsuarioDB(
                user=user, 
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                municipio_fk=self.cleaned_data['municipio_fk'],  # Guardar municipio
                direccion=self.cleaned_data['direccion'],
                imagen_perfil=self.cleaned_data.get('imagen_perfil')  # Guardar imagen de perfil si se sube
            )
            perfil.save()
        return user