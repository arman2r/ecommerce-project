# Generated by Django 3.0.4 on 2020-04-30 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoriasblog', '0001_initial'),
        ('blog', '0005_auto_20200430_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='categories', to='categoriasblog.Category', verbose_name='Categorías'),
        ),
    ]
