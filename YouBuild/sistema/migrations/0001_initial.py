# Generated by Django 5.1.1 on 2024-10-09 13:25

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarritoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Carrito',
                'verbose_name_plural': 'Carritos',
            },
        ),
        migrations.CreateModel(
            name='CarruselDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to='carrusel')),
            ],
            options={
                'verbose_name': 'Carrusel',
                'verbose_name_plural': 'Carruseles',
            },
        ),
        migrations.CreateModel(
            name='CategoriaDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, verbose_name='Nombre de la categoría')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
            },
        ),
        migrations.CreateModel(
            name='DepartamentoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre del departamento')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='TipoPagoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre_tipo_de_pago')),
            ],
            options={
                'verbose_name': 'TipoPago',
                'db_table': 'tipo_de_pago',
            },
        ),
        migrations.CreateModel(
            name='ProductoDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('detalle', models.TextField(max_length=200, verbose_name='Detalle')),
                ('precio', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(99999.9)], verbose_name='Precio')),
                ('visitas', models.PositiveIntegerField(default=0, verbose_name='Visitas')),
                ('cantidad', models.IntegerField(default=1)),
                ('categoria_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.categoriadb')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'productos',
            },
        ),
        migrations.CreateModel(
            name='ImagenProductoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to='productos')),
                ('producto_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='sistema.productodb')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='CarritoProductoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('carrito_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.carritodb')),
                ('producto_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.productodb')),
            ],
            options={
                'verbose_name': 'Carrito Producto',
                'verbose_name_plural': 'Carrito Productos',
            },
        ),
        migrations.CreateModel(
            name='ProvinciaDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre de la provincia')),
                ('departamento_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.departamentodb')),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.CreateModel(
            name='MunicipioDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre del municipio')),
                ('provincia_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.provinciadb')),
            ],
            options={
                'verbose_name': 'Municipio',
                'verbose_name_plural': 'Municipios',
            },
        ),
        migrations.CreateModel(
            name='UsuarioDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=100, verbose_name='Apellido')),
                ('contraseña', models.CharField(max_length=20, verbose_name='Contraseña')),
                ('fecha_nac', models.DateField(verbose_name='Fecha_de_nacimiento')),
                ('municipio_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.municipiodb')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.AddField(
            model_name='productodb',
            name='usuario_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.usuariodb'),
        ),
        migrations.CreateModel(
            name='PagoDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha_de_pago')),
                ('monto_pagado', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto Pagado')),
                ('carrito_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.carritodb')),
                ('tipo_pago_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.tipopagodb')),
                ('usuario_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.usuariodb')),
            ],
            options={
                'verbose_name_plural': 'pagos',
                'db_table': 'pago',
            },
        ),
        migrations.AddField(
            model_name='carritodb',
            name='usuario_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.usuariodb'),
        ),
    ]
