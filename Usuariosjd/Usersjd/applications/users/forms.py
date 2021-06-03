from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):
    # Nunca poner contraseñla como texto plano, hacerlo de la siguiente forma
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña'
            }
        )
    )

    class Meta:

        model = User
        fields = ('user_name', 'email', 'nombres', 'apellidos', 'genero')

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden')


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña'
            }
        )
    )
    # Con esto django sabe que es una de las primeras validaciones que deben aplicarse

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user_name = self.cleaned_data['user_name']
        password = self.cleaned_data['password']

        if not authenticate(user_name=user_name, password=password):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos')
        return self.cleaned_data


class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )

    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )


class VerificationForm(forms.Form):

    cod_registro = forms.CharField(max_length=6, required=True)
    # Aca haremos la validacion del codigo ingresado.

    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_cod_registro(self):
        codigo = self.cleaned_data['cod_registro']
        if len(codigo) == 6:
            # Verificamos si el codigo y el id de usuario son validos
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')

        else:
            raise forms.ValidationError('El codigo es incorrecto')


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
