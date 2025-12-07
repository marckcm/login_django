from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.conf import settings


def staff_member_required(view_func):
    """
    Decorador para views que verifica se o usuário está logado e é um membro da equipe (is_staff).
    """
    decorated_view = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='home',
        redirect_field_name=None
    )(view_func)
    return decorated_view


def anonymous_required(view_func):
    """
    Decorador para views que só devem ser acessíveis por usuários anônimos (não logados).
    Usuários autenticados são redirecionados para LOGIN_REDIRECT_URL.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return view_func(request, *args, **kwargs)
    return wrapper
