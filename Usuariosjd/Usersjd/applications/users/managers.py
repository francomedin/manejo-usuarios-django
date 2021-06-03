from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, user_name, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            user_name=user_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            ** extra_fields
        )
        # Por buena practica se necesita encriptar la password.
        user.set_password(password)
        # el using elig con que base de datos trabajaremos.
        user.save(using=self.db)
        return user

    def create_user(self, user_name, email, password=None, **extra_fields):
        return self._create_user(user_name, email, password, False, False, False, **extra_fields)

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        return self._create_user(user_name, email, password, True, True, True, ** extra_fields)

    def cod_validation(self, id_user, cod_validation):
        if self.filter(id=id_user, cod_registro=cod_validation).exists():
            return True
        else:
            return False
