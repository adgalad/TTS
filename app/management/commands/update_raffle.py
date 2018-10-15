#!/usr/bin/env python
import time

from django.contrib.auth.models import Permission, Group, ContentType
from django.core.management.base import BaseCommand

import app.models as models

class Command(BaseCommand):

    DELAY = 10

    def handle(self, *args, **options):
        pass
    
    
