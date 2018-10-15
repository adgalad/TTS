import json
import random
import threading
import os

from subprocess import check_output 
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.mail import send_mail
from django.core.files.base import ContentFile

from TTS.settings import DEFAULT_FROM_EMAIL, MEDIA_ROOT
from .watson_text_to_speech import text_to_specch
# Create your models here.

class EmailThread(threading.Thread):
    def __init__(self, subject, message, html_message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run (self):
        send_mail(subject=self.subject,
                  message=self.message,
                  html_message=self.html_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=self.recipient_list)

# def sendEmailLoser(user):
#     plain_message = "You didn't win the raffle."
#     html_message = "You didn't win the raffle."
#     EmailThread(subject="Verificación de correo electrónico",
#                   message=plain_message,
#                   html_message=html_message,
#                   recipient_list=[user.email]).start()




class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('verified', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    email = models.EmailField(unique=True, null=True)
    first_name   = models.CharField(unique=True, max_length=64, verbose_name='')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    username     = models.CharField(unique=True, max_length=64, verbose_name='Username')
    verified     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    objects = MyUserManager()


    def __str__(self):
        return self.email

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.username
    # @property
    # def id_back_url(self):
    #     if self.id_back and hasattr(self.id_back, 'url'):
    #         return self.id_back.url
    #     else:
    #         return '/static/images/placeholder.png'



def fileName(instance, filename):
    return 'audios/user_{0}/{1}'.format(instance.created_by.pk, filename)

class Audio(models.Model):

    name = models.CharField(unique=True, max_length=64, verbose_name='Nombre del archivo', help_text="Nombre del archivo en el que se guarda el audio generado.")
    format_choices=[('mp3','mp3'), ('wav','wav'), ('flac','flac'), ('ogg', 'ogg')]
    format = models.CharField(choices=format_choices, max_length=16, verbose_name='Formato')
    created_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Creación")
    status_choice = (('Aprobado','Aprobado'), ('En revisión','En revisión'))
    status = models.CharField(choices=status_choice, default="En revisión", max_length=64, verbose_name='Estado')
    description = models.CharField(max_length=256, null=True, blank=True, verbose_name='Descripción')
    text = models.CharField(max_length=512, verbose_name='Texto')
    audio_file = models.FileField(upload_to=fileName, null=True)
    created_by = models.ForeignKey(User, null=True, related_name='audios')


    def __str__(self):
        return "%s.%s"%(self.name, self.format)

    def save(self, *args, **kwargs):
        super(Audio, self).save(*args, **kwargs)

    def createAudio(self):
        rawAudio = text_to_specch.getRawAudio(self.text, "audio/%s"%self.format)
        print(self.audio_file, bool(self.audio_file))
        if bool(self.audio_file):
            os.remove(self.audio_file.path)
        self.audio_file.save("%s.%s"%(self.name, self.format), ContentFile(rawAudio))
    
    def delete(self, *args, **kwargs):
        self.audio_file.delete()
        super(Audio, self).delete(*args, **kwargs)

    @property
    def url(self):
        return "/media/" + fileName(self, "%s.%s"%(self.name, self.format))




        