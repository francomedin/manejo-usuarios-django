from django.db import models


class CuentaManager(models.Manager):
    def create_cuenta(self, tipo, codigo, usuario, **extra_fields):
        cuenta = self.model(
            tipo=tipo,
            codigo=codigo,
            usuario=usuario,
            ** extra_fields
        )

        cuenta.save(using=self.db)
        return cuenta
