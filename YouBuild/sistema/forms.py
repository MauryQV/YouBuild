from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UsuarioDB


class LoginForm(AuthenticationForm):
    pass

class RegistroUsuarioForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    tipo_usuario = forms.ChoiceField(choices=UsuarioDB.USUARIO_TIPOS)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'fecha_nacimiento', 'tipo_usuario']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear perfil de usuario
            perfil = UsuarioDB(user=user, fecha_nacimiento=self.cleaned_data['fecha_nacimiento'], tipo_usuario=self.cleaned_data['tipo_usuario'])
            perfil.save()
        return user
# Vista principal