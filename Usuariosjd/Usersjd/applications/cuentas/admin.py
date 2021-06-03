from django.contrib import admin
from .models import Cuenta
# Register your models here.

admin.site.register(Cuenta)

#Hacer que la cuenta asociada solo sea visible y no se pued editar desde el admin.