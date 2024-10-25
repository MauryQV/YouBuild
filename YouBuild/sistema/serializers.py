from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UsuarioDB

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioDB
        fields = ['user', 'fecha_nacimiento', 'municipio_fk', 'direccion', 'imagen_perfil']
