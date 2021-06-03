
# El view es la vista mas simple.
from django.db.models import fields
from django.views.generic import UpdateView, View, DetailView, TemplateView
from django.views.generic.edit import FormView
from .models import User
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,
    ResetPasswordForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .functions import code_generator
from django.core.mail import send_mail
# Esto automatiza el login
from django.contrib.auth import authenticate, login, logout


class HomeTemplateView(TemplateView):
    template_name = "users/home.html"


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = '/'

    def form_valid(self, form):
        # generamos el codigo
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['user_name'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            cod_registro=codigo
        )
        # Se envia el email con el codigo generado.
        asunto = 'Confirmacion de Email'
        mensaje = 'Codigo de verificacion: ' + codigo
        email_remitente = 'franco.medinna@gmail.com'
        send_mail(asunto, mensaje, email_remitente,
                  [form.cleaned_data['email'], ])
        # Una vez enviado el mail se debe ir a una pantalla para que el usuario ingrese el codigo recibido.
        return HttpResponseRedirect(
            reverse(
                'users_app:users_verification',
                # Se asocia el codigo al id.
                # Enviamos datos por contexto
                kwargs={'pk': usuario.id}

            )
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('users_app:home')

    def form_valid(self, form):
        # Esto hace el login y manteniene la session.
        user = authenticate(
            user_name=form.cleaned_data['user_name'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        # Cuando complete el proceso de logou me redireccione
        return HttpResponseRedirect(
            reverse(
                'users_app:users_login'
            )
        )


class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:users_login')
    login_url = reverse_lazy('users_app:users_login')

    def form_valid(self, form):
        # Con el siguiente request obtengo el usuario de la sesion.Siempre
        usuario = self.request.user
        user = authenticate(
            user_name=usuario.user_name,
            password=form.cleaned_data['password1']
        )
        # Si el usuario es valido entonces:
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            print('guardado correctamente')

        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:home')

    # Como los forms no pueden hacer uso de los kwargs se los tengo que pasar de esta manera.
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)


class UsersUpdateView(UpdateView):
    model = User
    template_name = "users/update_profile.html"
    fields = ['nombres', 'apellidos', 'email']


class UserDetailView(DetailView):
    model = User
    template_name = "users/profile.html"


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'users/password_recovery.html'
    success_url = reverse_lazy('users_app:users_login')

    def form_valid(self, form):
        # Creamos un codigo
        codigo = code_generator()
        # Filtramos el usuario por el mail ingresado
        usuario = User.objects.get(email=form.cleaned_data['email'])
        # Seteamos la nueva contraseña al usuario
        usuario.set_password(codigo)
        usuario.save()
        # Enviar el mail con la contraseña nueva
        asunto = 'Reseteo de Contraseña'
        mensaje = 'Nueva contraseña: ' + codigo
        email_remitente = 'franco.medinna@gmail.com'
        send_mail(asunto, mensaje, email_remitente,
                  [form.cleaned_data['email'], ])
        return super(ResetPasswordView, self).form_valid(form)


