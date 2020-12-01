# Generated by Django 3.0.4 on 2020-05-19 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dastosUsuario', '0004_remove_datos_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datos',
            name='email',
        ),
        migrations.RemoveField(
            model_name='datos',
            name='first_sname',
        ),
        migrations.RemoveField(
            model_name='datos',
            name='last_name',
        ),
        migrations.AddField(
            model_name='datos',
            name='usuario',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
            preserve_default=False,
        ),
    ]