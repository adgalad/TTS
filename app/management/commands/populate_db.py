#!/usr/bin/env python
import time

from django.contrib.auth.models import Permission, Group, ContentType
from django.core.management.base import BaseCommand

import app.models as models

class Command(BaseCommand):

    def createPermissions(self):

        Permission.objects.all().delete()
        ContentType.objects.all().delete()
        Group.objects.all().delete()

        audio = ContentType.objects.create(app_label='tts', model='Audio')

        
        download_audio = Permission.objects.create(name='Descargar',  codename='can_download',  content_type=audio)
        create_audio = Permission.objects.create(name='Crear', codename='can_create', content_type=audio)
        aprove_audio = Permission.objects.create(name='Aprobar', codename='can_aprove', content_type=audio)
        edit_audio = Permission.objects.create(name='Editar', codename='can_edit', content_type=audio)
        hear_audio = Permission.objects.create(name='Escuchar', codename='can_hear', content_type=audio)

        P1 = Group.objects.create(name='Perfil 1')
        P2 = Group.objects.create(name='Perfil 2')
        P3 = Group.objects.create(name='Perfil 3')
        
        P1.permissions.add(download_audio)
        P1.permissions.add(hear_audio)
        P1.permissions.add(edit_audio)
        P1.permissions.add(create_audio)
        P1.permissions.add(aprove_audio)

        P2.permissions.add(download_audio)
        P2.permissions.add(hear_audio)

        P2.permissions.add(create_audio)
        P2.permissions.add(hear_audio)


        


    def handle(self, *args, **options):
        pass
    
    
