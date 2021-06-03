from applications.users.models import User
from django.db import models
from django.urls.base import reverse
from .managers import CuentaManager


class Cuenta(models.Model):
    ACCOUNT_TYPE = (
        ('C', 'Billetera Cripto'),
        ('B', 'Banco'),
    )
    tipo = models.CharField(max_length=1, choices=ACCOUNT_TYPE)
    codigo = models.CharField(max_length=100)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    objects = CuentaManager()

    def get_absolute_url(self):
        return reverse('cuenta_app:cuenta_detail', kwargs={'pk': self.pk})
