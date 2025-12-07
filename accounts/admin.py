
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PasswordResetToken, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    # Campos a serem exibidos na lista de usuários
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_2fa_enabled')
    # Campos para busca
    search_fields = ('email', 'username', 'first_name', 'last_name')
    # Campos para filtro
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # Organização dos campos no formulário de edição
    fieldsets = UserAdmin.fieldsets + ((
        'Autenticação de Dois Fatores', {'fields': ('is_2fa_enabled', 'otp_secret')}
    ),)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin configuration for the PasswordResetToken model."""
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
