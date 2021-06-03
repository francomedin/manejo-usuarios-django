from django.forms import models
from .models import Cuenta


class CuentaForm(models.ModelForm):

    class Meta:
        model = Cuenta
        fields = ('tipo', 'codigo')
