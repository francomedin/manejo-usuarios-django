from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
import datetime


class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "practica/index.html"
    # El login nos pide que creemos
    login_url = reverse_lazy('users_app:users_login')


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "practica/mixin.html"
