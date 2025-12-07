from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text='Digite um endereço de e-mail válido'
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label='Nome',
        help_text='Digite seu primeiro nome'
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label='Sobrenome',
        help_text='Digite seu sobrenome'
    )
    username = forms.CharField(
        label='Nome de usuário',
        help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='Senha',
        help_text='Sua senha deve conter pelo menos 8 caracteres.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmar senha',
        help_text='Digite a mesma senha novamente para verificação.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'password1', 'password2']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
        label='Senha'
    )


class TwoFactorForm(forms.Form):
    token = forms.CharField(
        max_length=6,
        min_length=6,
        label='Código de verificação',
        widget=forms.TextInput(attrs={'placeholder': '000000'}),
        help_text='Digite o código de 6 dígitos do seu aplicativo autenticador'
    )


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Nome de usuário')
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    phone = forms.CharField(label='Telefone', required=False)
    is_active = forms.BooleanField(label='Ativo', required=False)
    is_staff = forms.BooleanField(label='Equipe', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'phone', 'is_active', 'is_staff']


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
        help_text='Digite o e-mail associado à sua conta'
    )


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Nova Senha')
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Confirmar Senha')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem')
        return cleaned_data
