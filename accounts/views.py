from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import staff_member_required, anonymous_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import User, PasswordResetToken
from .forms import *
import secrets

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@anonymous_required
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # O EmailBackend configurado em settings.py cuidará da autenticação
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_2fa_enabled:
                    request.session['pre_2fa_user_id'] = user.id
                    return redirect('verify_2fa')
                else:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'E-mail ou senha inválidos. Por favor, tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def verify_2fa_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        messages.error(request, 'Sessão de login inválida. Por favor, faça o login novamente.')
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if user.verify_totp(token):
                del request.session['pre_2fa_user_id']
                login(request, user) # O backend já foi determinado na autenticação inicial
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Código inválido')
    else:
        form = TwoFactorForm()

    return render(request, 'accounts/verify_2fa.html', {'form': form})


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


@login_required
def setup_2fa_view(request):
    user = request.user

    if not user.otp_secret:
        user.generate_otp_secret()

    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if user.verify_totp(token):
                user.is_2fa_enabled = True
                user.save()
                messages.success(request, '2FA ativado com sucesso!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Código inválido')
    else:
        form = TwoFactorForm()

    qr_code = user.get_qr_code()
    return render(request, 'accounts/setup_2fa.html', {
        'form': form,
        'qr_code': qr_code,
        'secret': user.otp_secret
    })


@login_required
def disable_2fa_view(request):
    if request.method == 'POST':
        request.user.is_2fa_enabled = False
        request.user.save()
        messages.success(request, '2FA desativado')
        return redirect('dashboard')
    return render(request, 'accounts/disable_2fa.html')


@staff_member_required
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@staff_member_required
def user_create_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('user_list')

    form = UserRegistrationForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Criar Usuário'})


@staff_member_required
def user_update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('user_list')

    form = UserUpdateForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Editar Usuário'})


@staff_member_required
def user_delete_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})


def password_reset_request_view(request):
    # Verifica se está usando console backend
    is_console_backend = 'console' in settings.EMAIL_BACKEND.lower()
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = secrets.token_urlsafe(32)

                PasswordResetToken.objects.create(user=user, token=token)

                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', args=[token])
                )

                try:
                    send_mail(
                        'Redefinição de Senha',
                        f'Clique no link para redefinir sua senha: {reset_url}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    
                    # Se estiver usando console backend, mostra o link na página
                    if is_console_backend:
                        messages.info(request,
                            '⚠️ Modo Desenvolvimento: Email não foi enviado. '
                            'Verifique o console do servidor ou use o link abaixo.')
                        return render(request, 'accounts/password_reset_request.html', {
                            'form': form,
                            'reset_url': reset_url,
                            'is_console_backend': True
                        })
                    else:
                        messages.success(request,
                            'Email de redefinição de senha enviado com sucesso! '
                            'Verifique sua caixa de entrada (e a pasta de spam).')
                except Exception as e:
                    messages.error(request,
                        f'Erro ao enviar e-mail: {str(e)}. '
                        'Verifique as configurações de e-mail.')
                    return render(request, 'accounts/password_reset_request.html', {
                        'form': form,
                        'is_console_backend': is_console_backend
                    })
            except User.DoesNotExist:
                # Não revela se o usuário existe ou não.
                # Apenas continue, a mensagem de sucesso será mostrada de qualquer forma.
                pass

            # Se chegou aqui e não mostrou mensagem acima, mostra mensagem genérica
            if not is_console_backend:
                messages.success(request,
                    'Se um usuário com esse e-mail existir, um link para redefinição de senha foi enviado.')
            return redirect('home')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset_request.html', {
        'form': form,
        'is_console_backend': is_console_backend
    })


def password_reset_confirm_view(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        if not reset_token.is_valid():
            messages.error(request, 'Token inválido ou expirado')
            return redirect('password_reset_request')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Token inválido')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = reset_token.user
            user.set_password(password)
            user.save()

            reset_token.is_used = True
            reset_token.save()

            messages.success(request, 'Senha redefinida com sucesso!')
            return redirect('home')
    else:
        form = PasswordResetConfirmForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
