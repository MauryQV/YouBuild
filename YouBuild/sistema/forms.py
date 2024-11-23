from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import UsuarioDB, ProductoDb, CategoriaDb, DepartamentoDB, ProvinciaDB, MunicipioDB, ImagenProductoDB, SubcategoriaDB
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
import re

class LoginForm(AuthenticationForm):
    pass


class RegistroUsuarioForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=255, 
        required=True, 
        label="Nombre completo",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre completo'})
    )
    email = forms.EmailField(
        required=True,
        label="Correo electrónico (opcional)",  
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu correo electrónico'})
    )
    departamento_fk = forms.ModelChoiceField(
        queryset=DepartamentoDB.objects.all(), 
        required=True, 
        label="Departamento",
        widget=forms.Select(attrs={'placeholder': 'Selecciona tu departamento'})
    )
    provincia_fk = forms.ModelChoiceField(
        queryset=ProvinciaDB.objects.none(), 
        required=True, 
        label="Provincia",
        widget=forms.Select(attrs={'placeholder': 'Selecciona tu provincia'})
    )
    municipio_fk = forms.ModelChoiceField(
        queryset=MunicipioDB.objects.none(), 
        required=True, 
        label="Municipio",
        widget=forms.Select(attrs={'placeholder': 'Selecciona tu municipio'})
    )
    direccion_1 = forms.CharField(
        max_length=255, 
        required=True, 
        label="Dirección",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu dirección'})
    )
    telefono = forms.CharField(
        max_length=15, 
        required=True, 
        label="Número de celular",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu número de celular'})
    )
    imagen_perfil = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'placeholder': 'Selecciona tu foto de perfil'})
    )
    qr_imagen = forms.ImageField(
        required=False, 
        label="Código QR",
        widget=forms.FileInput(attrs={'placeholder': 'Selecciona la imagen QR'})
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'nombre_completo', 'departamento_fk', 'provincia_fk', 'municipio_fk',
            'direccion_1', 'telefono',
            'imagen_perfil', 'qr_imagen'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Ingresa tu nombre de usuario'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Ingresa tu correo electrónico'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Ingresa tu contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirma tu contraseña'})

        if 'departamento_fk' in self.data:
            try:
                departamento_id = int(self.data.get('departamento_fk'))
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
            except (ValueError, TypeError):
                pass

        if 'provincia_fk' in self.data:
            try:
                provincia_id = int(self.data.get('provincia_fk'))
                self.fields['municipio_fk'].queryset = MunicipioDB.objects.filter(provincia_fk=provincia_id).order_by('nombre')
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
        if commit:
            user.save()
            UsuarioDB.objects.create(
                user=user,
                nombre_completo=self.cleaned_data['nombre_completo'],
                municipio_fk=self.cleaned_data['municipio_fk'],
                direccion_1=self.cleaned_data['direccion_1'],
                telefono=self.cleaned_data['telefono'],
                imagen_perfil=self.cleaned_data.get('imagen_perfil') or 'perfil/perfil.png',
                qr_imagen=self.cleaned_data.get('qr_imagen')
            )
        return user
    
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False  # Oculta etiquetas para tener un diseño más limpio
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Guardar Cambios', css_class='btn-primario')
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Correo electronico ya registrado.")
        return email
    
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UsuarioDB
        fields = ['nombre_completo', 'direccion_1']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'nombre_completo',
            'direccion_1',
            Submit('submit', 'Actualizar Perfil', css_class='btn-primario')
        )
    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        # Verificar que el nombre contenga solo letras y espacios
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]+$", nombre):
            raise forms.ValidationError("El nombre solo puede contener letras")
        return nombre



class RegistroProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre del producto",
        widget=forms.TextInput(attrs={'placeholder': '--Agrega el nombre del producto--'})
    )
    detalle = forms.CharField(
        max_length=500,
        required=True,
        label="Detalle",
        widget=forms.Textarea(attrs={'placeholder': '--Agrega más detalles del producto--'})
    )
    precio = forms.FloatField(
        required=True,
        label="Precio",
        widget=forms.NumberInput(attrs={'placeholder': '00.00'})
    )
    categoria_fk = forms.ModelChoiceField(
        queryset=CategoriaDb.objects.all(),
        required=True,
        label="Categoría",
        widget=forms.Select(attrs={'placeholder': 'Selecciona una categoría'})
    )
    departamento_fk = forms.ModelChoiceField(
        queryset=DepartamentoDB.objects.all(),
        required=True,
        label="Departamento",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un departamento'})
    )
    provincia_fk = forms.ModelChoiceField(
        queryset=ProvinciaDB.objects.none(),
        required=True,
        label="Provincia",
        widget=forms.Select(attrs={'placeholder': 'Selecciona una provincia'})
    )
    municipio_fk = forms.ModelChoiceField(
        queryset=MunicipioDB.objects.all(),
        required=True,
        label="Municipio",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un municipio'})
    )
    direccion_1 = forms.CharField(
        max_length=255,
        required=True,
        label="Dirección",
        widget=forms.TextInput(attrs={'placeholder': '--Agrega más detalles de la ubicación, puntos de referencia, nro de casa, etc.--'})
    )
    cantidad = forms.IntegerField(
        required=True,
        initial=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'placeholder': 'Ingresa la cantidad del producto'})
    )
    imagenes = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(),  # No uses multiple=True aquí
        label="Imágenes"
    )

    class Meta:
        model = ProductoDb
        fields = [
            'nombre', 'detalle', 'precio', 'categoria_fk',
            'departamento_fk', 'provincia_fk', 'municipio_fk', 
            'direccion_1', 'cantidad', 'imagenes'
        ]

    def clean_imagenes(self):
        imagenes = self.files.getlist('imagenes')
        if not (1 <= len(imagenes) <= 4):
            raise forms.ValidationError("Debes subir entre 1 y 4 imágenes.")
        if not all(img.name.lower().endswith(('.png', '.jpg', '.jpeg')) for img in imagenes):
            raise forms.ValidationError("Solo se permiten archivos con formato .png, .jpg, o .jpeg.")
        return imagenes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:  # Solo ocurre cuando se está editando un producto
            municipio = self.instance.municipio_fk
            provincia = municipio.provincia_fk
            departamento = provincia.departamento_fk
            
            # Llenamos las opciones correspondientes para el formulario de edición
            self.fields['departamento_fk'].initial = departamento
            self.fields['provincia_fk'].initial = provincia
            self.fields['municipio_fk'].initial = municipio
            
            # Filtrar provincias según el departamento del municipio
            self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=departamento).order_by('nombre')
            
            # Filtrar municipios según la provincia del municipio
            self.fields['municipio_fk'].queryset = MunicipioDB.objects.filter(provincia_fk=provincia).order_by('nombre')
        
        elif 'departamento_fk' in self.data:
            # Lógica de creación, como estaba antes
            try:
                departamento_id = int(self.data.get('departamento_fk'))
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=departamento_id).order_by('nombre')
            except (ValueError, TypeError):
                pass


@transaction.atomic
def save(self, commit=True):
    producto = super().save(commit=False)  # El objeto no se guarda aún en la base de datos
    if commit:
        producto.save()  # Aquí se guarda el producto y se genera su primary key
        for imagen in self.cleaned_data.get('imagenes'):  # Intentas acceder a una relación
            ImagenProductoDB.objects.create(producto_fk=producto, imagen=imagen)  # Esto requiere un PK
    return producto



class EditarProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=50,
        required=True,
        label="Nombre del producto",
        widget=forms.TextInput(attrs={'placeholder': '--Modifica el nombre del producto--'})
    )
    detalle = forms.CharField(
        max_length=500,
        required=True,
        label="Descripción",
        widget=forms.Textarea(attrs={'placeholder': '--Modifica la descripción del producto--'})
    )
    precio = forms.FloatField(
        required=True,
        label="Precio",
        widget=forms.NumberInput(attrs={'placeholder': '00.00'})
    )
    categoria_fk = forms.ModelChoiceField(
        queryset=CategoriaDb.objects.all(),
        required=True,
        label="Categoría",
        widget=forms.Select(attrs={'placeholder': 'Selecciona una categoría'})
    )
    subcategoria_fk = forms.ModelChoiceField(
        queryset=SubcategoriaDB.objects.all(),
        required=True,
        label="Subcategoría",
        widget=forms.Select(attrs={'placeholder': 'Selecciona una subcategoría'})
    )
    departamento_fk = forms.ModelChoiceField(
        queryset=DepartamentoDB.objects.all(),
        required=True,
        label="Departamento",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un departamento'})
    )
    provincia_fk = forms.ModelChoiceField(
        queryset=ProvinciaDB.objects.none(),
        required=True,
        label="Provincia",
        widget=forms.Select(attrs={'placeholder': 'Selecciona una provincia'})
    )
    municipio_fk = forms.ModelChoiceField(
        queryset=MunicipioDB.objects.none(),
        required=True,
        label="Municipio",
        widget=forms.Select(attrs={'placeholder': 'Selecciona un municipio'})
    )
    direccion_1 = forms.CharField(
        max_length=255,
        required=True,
        label="Dirección",
        widget=forms.TextInput(attrs={'placeholder': '--Modifica la dirección del producto--'})
    )
    cantidad = forms.IntegerField(
        required=True,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'placeholder': 'Ingresa la cantidad del producto'})
    )
    imagenes = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(),  # No uses multiple=True aquí
        label="Imágenes"
    )

    class Meta:
        model = ProductoDb
        fields = [
            'nombre', 'detalle', 'precio', 'categoria_fk', 'subcategoria_fk', 
            'departamento_fk', 'provincia_fk', 'municipio_fk', 'direccion_1', 
            'cantidad', 'imagenes'
        ]

    def clean_imagenes(self):
        imagenes = self.files.getlist('imagenes')
        if imagenes and not (1 <= len(imagenes) <= 4):
            raise forms.ValidationError("Debes subir entre 1 y 4 imágenes.")
        if imagenes and not all(img.name.lower().endswith(('.png', '.jpg', '.jpeg')) for img in imagenes):
            raise forms.ValidationError("Solo se permiten archivos con formato .png, .jpg, o .jpeg.")
        return imagenes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Obtener municipio, provincia y departamento relacionados
            municipio = self.instance.municipio_fk
            if municipio:
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=municipio.provincia_fk.departamento_fk)
                self.fields['departamento_fk'].queryset = DepartamentoDB.objects.all()

                # Establecer el departamento y la provincia al producto actual
                self.instance.provincia_fk = municipio.provincia_fk
                self.instance.departamento_fk = municipio.provincia_fk.departamento_fk

        # Si se está enviando datos, actualizar los campos de provincia y municipio
        if 'municipio_fk' in self.data:
            try:
                municipio_id = int(self.data.get('municipio_fk'))
                municipio = MunicipioDB.objects.get(id=municipio_id)
                self.fields['provincia_fk'].queryset = ProvinciaDB.objects.filter(departamento_fk=municipio.provincia_fk.departamento_fk)
                self.fields['departamento_fk'].queryset = DepartamentoDB.objects.all()
            except (ValueError, TypeError, MunicipioDB.DoesNotExist):
                pass

class OfertaForm(forms.ModelForm):
    producto_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)  # Campo oculto para el ID del producto

    class Meta:
        model = ProductoDb
        fields = ['descuento']  # Solo el descuento se va a modificar

    def clean_descuento(self):
        descuento = self.cleaned_data['descuento']
        if descuento < 0 or descuento > 100:
            raise forms.ValidationError("El descuento debe estar entre 0 y 100.")
        return descuento

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación para asegurarse de que producto_id es válido
        producto_id = cleaned_data.get("producto_id")
        if producto_id:
            try:
                producto = ProductoDb.objects.get(id=producto_id)
                if producto.estado != 'disponible':
                    raise forms.ValidationError("El producto debe estar disponible para crear una oferta.")
            except ProductoDb.DoesNotExist:
                raise forms.ValidationError("El producto seleccionado no existe.")
        
        return cleaned_data
