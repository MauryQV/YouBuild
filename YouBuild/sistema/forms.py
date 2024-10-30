from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import UsuarioDB, MunicipioDB, ProvinciaDB, DepartamentoDB
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

class LoginForm(AuthenticationForm):
    pass

class RegistroUsuarioForm(UserCreationForm):
    nombre_completo = forms.CharField(max_length=255, required=True, label="Nombre completo")
    nombre_usuario = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    direccion_1 = forms.CharField(max_length=255, required=True, label="Dirección")
    telefono = forms.CharField(max_length=15, required=True, label="Número de teléfono")
    correo = forms.EmailField(required=True, label="Correo electrónico")
    departamento_fk = forms.ModelChoiceField(queryset=DepartamentoDB.objects.all(), required=True, label="Departamento")
    provincia_fk = forms.ModelChoiceField(queryset=ProvinciaDB.objects.none(), required=True, label="Provincia")
    municipio_fk = forms.ModelChoiceField(queryset=MunicipioDB.objects.none(), required=True, label="Municipio")
    imagen_perfil = forms.ImageField(required=False)
    qr_imagen = forms.ImageField(required=False, label="Código QR")

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'nombre_completo', 'nombre_usuario', 'departamento_fk', 'provincia_fk', 
            'municipio_fk', 'direccion_1', 'telefono', 'correo',
            'imagen_perfil', 'qr_imagen'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Actualizar el queryset de Provincia basado en Departamento seleccionado
        departamento_id = self.data.get('departamento_fk') or (self.instance.pk and self.instance.municipio_fk.provincia_fk.departamento_fk.id)
        if departamento_id:
            try:
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=int(departamento_id)).order_by('nombre')
            except (ValueError, TypeError):
                pass

        # Actualizar el queryset de Municipio basado en Provincia seleccionada
        provincia_id = self.data.get('provincia_fk') or (self.instance.pk and self.instance.municipio_fk.provincia_fk.id)
        if provincia_id:
            try:
                self.fields['municipio_fk'].queryset = MunicipioDB.objects.filter(provincia_fk=int(provincia_id)).order_by('nombre')
            except (ValueError, TypeError):
                pass

    def clean_imagen_perfil(self):
        imagen = self.cleaned_data.get('imagen_perfil')
        if imagen and not imagen.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Solo se permiten archivos con formato .png, .jpg, o .jpeg.")
        return imagen

    def clean_qr_imagen(self):
        qr = self.cleaned_data.get('qr_imagen')
        if qr and not qr.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Solo se permiten archivos con formato .png, .jpg, o .jpeg para el Código QR.")
        return qr

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        try:
            if commit:
                user.save()
                UsuarioDB.objects.create(
                    user=user,
                    nombre_completo=self.cleaned_data['nombre_completo'],
                    nombre_usuario=self.cleaned_data['nombre_usuario'],  # Asegúrate de que este campo exista en UsuarioDB
                    municipio_fk=self.cleaned_data['municipio_fk'],
                    direccion_1=self.cleaned_data['direccion_1'],
                    telefono=self.cleaned_data['telefono'],
                    correo=self.cleaned_data['correo'],  # Asegúrate de que este campo exista en UsuarioDB
                    imagen_perfil=self.cleaned_data.get('imagen_perfil') or 'perfil/perfil.png',  # Imagen por defecto
                    qr_imagen=self.cleaned_data.get('qr_imagen')
                )
        except Exception as e:
            raise ValidationError(f"Ocurrió un error al guardar los datos: {str(e)}")
        return user
