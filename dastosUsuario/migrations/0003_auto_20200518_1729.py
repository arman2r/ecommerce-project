# Generated by Django 3.0.4 on 2020-05-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dastosUsuario', '0002_datos_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos',
            name='Shipping_Address',
            field=models.CharField(default=2, max_length=50, verbose_name='Dirección de envio'),
            preserve_default=False,
        ),
    ]