from django.contrib.auth.models import AbstractUser
from django.db import models
import pyotp
import qrcode
from io import BytesIO
import base64
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    is_2fa_enabled = models.BooleanField(default=False, verbose_name='2FA Habilitado')
    otp_secret = models.CharField(max_length=32, blank=True, null=True, verbose_name='Segredo OTP')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def generate_otp_secret(self):
        """Gera um novo segredo OTP"""
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()
        return self.otp_secret

    def get_totp_uri(self):
        """Retorna URI para gerar QR Code"""
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            name=self.email,
            issuer_name='Django 2FA App'
        )

    def verify_totp(self, token):
        """Verifica token TOTP"""
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token, valid_window=1)

    def get_qr_code(self):
        """Gera QR Code em base64"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.get_totp_uri())
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    token = models.CharField(max_length=100, unique=True, verbose_name='Token')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    is_used = models.BooleanField(default=False, verbose_name='Usado')
    
    class Meta:
        verbose_name = 'Token de Redefinição de Senha'
        verbose_name_plural = 'Tokens de Redefinição de Senha'

    def is_valid(self):
        """Verifica se token ainda é válido (24 horas)"""
        return not self.is_used and \
            (timezone.now() - self.created_at) < timedelta(hours=24)

