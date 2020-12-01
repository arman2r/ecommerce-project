# Generated by Django 3.0.3 on 2020-05-18 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_sname', models.CharField(max_length=50, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('whatsapp', models.CharField(max_length=12, verbose_name='Whatsapp')),
                ('idenfication', models.CharField(blank=True, max_length=50, null=True, verbose_name='C.C o Nit')),
                ('Shipping_Address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Dirección de envio')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Dato',
                'verbose_name_plural': 'Datos',
                'ordering': ['-created'],
            },
        ),
    ]