# Generated by Django 5.1.1 on 2024-10-24 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carritodb',
            options={},
        ),
        migrations.AlterModelOptions(
            name='carritoproductodb',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='carritoproductodb',
            name='unique_producto_en_carrito',
        ),
    ]
