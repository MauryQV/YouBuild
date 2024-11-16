from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UsuarioDB, ProductoDb

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hasheamos la contraseña
        user.save()
        return user

class UsuarioDBSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UsuarioDB
        fields = ['user', 'nombre_completo', 'municipio_fk', 'direccion_1', 'telefono', 'imagen_perfil', 'qr_imagen']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        # Creamos UsuarioDB y guardamos las imágenes si están presentes
        usuario_db = UsuarioDB.objects.create(user=user, **validated_data)
        return usuario_db

class ProductoSerializer(serializers.ModelSerializer):
    imagenes = serializers.StringRelatedField(many=True)
    categoria = serializers.StringRelatedField()
    subcategoria = serializers.StringRelatedField()

    class Meta:
        model = ProductoDb
        fields = ['id', 'nombre', 'detalle', 'precio', 'estado', 'imagenes', 'municipio_fk', 'categoria', 'subcategoria']