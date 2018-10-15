# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-15 16:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180815_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Nombre del archivo')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de Creación')),
                ('status', models.CharField(choices=[('Aprobado', 'Aprobado'), ('En revisión', 'En revisión')], default='En revisión', max_length=64, verbose_name='Estado')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Descripción')),
                ('text', models.CharField(max_length=516, verbose_name='Texto')),
                ('audio_file', models.FileField(upload_to='')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='record',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
    ]
