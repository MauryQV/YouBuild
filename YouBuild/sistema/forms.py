from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UsuarioDB,MunicipioDB,ProvinciaDB,DepartamentoDB
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction

class LoginForm(AuthenticationForm):
    pass


class RegistroUsuarioForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    departamento_fk = forms.ModelChoiceField(queryset=DepartamentoDB.objects.all(), required=True, label="Departamento")
    provincia_fk = forms.ModelChoiceField(queryset=ProvinciaDB.objects.none(), required=True, label="Provincia")
    municipio_fk = forms.ModelChoiceField(queryset=MunicipioDB.objects.none(), required=True, label="Municipio")
    direccion = forms.CharField(max_length=255, required=True)
    imagen_perfil = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'fecha_nacimiento', 'departamento_fk', 'provincia_fk', 'municipio_fk', 'direccion', 'imagen_perfil']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si se pasa un departamento, inicializa el queryset de provincias
        if 'departamento_fk' in self.data:
            try:
                departamento_id = int(self.data.get('departamento_fk'))
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=self.instance.municipio_fk.provincia_fk.departamento_fk).order_by('nombre')

        # Si se pasa una provincia, inicializa el queryset de municipios
        if 'provincia_fk' in self.data:
            try:
                provincia_id = int(self.data.get('provincia_fk'))
                self.fields['municipio_fk'].queryset = MunicipioDB.objects.filter(provincia_fk=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['municipio_fk'].queryset = MunicipioDB.objects.filter(provincia_fk=self.instance.municipio_fk.provincia_fk).order_by('nombre')

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento > timezone.now().date():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fecha_nacimiento

    def clean_imagen_perfil(self):
        imagen = self.cleaned_data.get('imagen_perfil')
        if imagen and not imagen.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Solo se permiten archivos con formato .png, .jpg, o .jpeg.")
        return imagen

    @transaction.atomic  # Para asegurarnos de que se completan todas las operaciones juntas
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # Guardamos el usuario en la tabla auth_user
            
            # Creamos el perfil en UsuarioDB
            perfil = UsuarioDB.objects.create(
                user=user,
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                municipio_fk=self.cleaned_data['municipio_fk'],
                direccion=self.cleaned_data['direccion'],
                imagen_perfil=self.cleaned_data.get('imagen_perfil')
            )
        return user
