from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls.base import reverse
from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros'),
    )
    user_name = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    cod_registro = models.CharField(max_length=6, blank=True)

    # Si puede o no entrar al admin de django
    is_staff = models.BooleanField(default=False)
    # Este atributo ya existe en el abastract.El usuario no esta activo hasta que se verifique
    is_active = models.BooleanField(default=False)
    # Que establecer como username en el login
    USERNAME_FIELD = 'user_name'
    # Asocial el archivo managers.
    objects = UserManager()
    # Datos obligatorios
    REQUIRED_FIELDS = ['email', ]

    def get_short_name(self):
        return self.user_name

    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos

    # Con este metodo, luego de editar me va a redirigir a un detail view.
    def get_absolute_url(self):
        return reverse('users_app:profile', kwargs={'pk': self.pk})
