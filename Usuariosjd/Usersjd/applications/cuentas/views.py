from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.views.generic.edit import FormView
from .models import Cuenta
from django.urls import reverse_lazy
from .forms import CuentaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from applications.users.models import User
# Create your views here.


class CuentaCreateView(LoginRequiredMixin, FormView):
    form_class = CuentaForm
    template_name = "cuentas/cuenta_create.html"
    success_url = reverse_lazy('cuenta_app:cuenta_list')

    def form_valid(self, form):
        # Aca asignar el usuario logeado a la cuenta que estoy creando.
        usuario = self.request.user
        Cuenta.objects.create_cuenta(
            tipo=form.cleaned_data['tipo'],
            codigo=form.cleaned_data['codigo'],
            usuario=usuario

        )

        return super(CuentaCreateView, self).form_valid(form)


class CuentaDetailView(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = "cuentas/cuenta_detail.html"
    fields = ['tipo', 'codigo']


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    template_name = "cuentas/cuenta_update.html"
    fields = ('tipo', 'codigo')


class CuentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = "cuentas/cuenta_delete.html"
    success_url = reverse_lazy('cuenta_app:cuenta_list')


class CuentaListView(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = "cuentas/cuenta_list.html"
    context_object_name = 'cuentas'
