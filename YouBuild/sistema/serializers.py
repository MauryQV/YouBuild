"""from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UsuarioDB

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    # Incluimos los campos de User y UsuarioDB
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    nombre_completo = serializers.CharField(required=True)
    fecha_nacimiento = serializers.DateField(required=True)
    direccion_1 = serializers.CharField(required=True)
    direccion_2 = serializers.CharField(required=True)
    telefono = serializers.CharField(required=True)
    
    # Campos para las imágenes
    imagen_perfil = serializers.ImageField(required=False, allow_null=True)
    qr_imagen = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = UsuarioDB
        fields = [
            'username', 'password', 'email', 'nombre_completo', 
            'fecha_nacimiento', 'direccion_1','direccion_2', 'telefono', 
            'imagen_perfil', 'qr_imagen'
        ]

    def create(self, validated_data):
        # Extraemos datos de User
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'email': validated_data.pop('email')
        }
        user = User.objects.create_user(**user_data)

        # Creamos el perfil del usuario (UsuarioDB) con imágenes
        usuario_db = UsuarioDB.objects.create(user=user, **validated_data)
        
        return usuario_db
"""