from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='home'), # Define a view de login como a página inicial
    path('accounts/', include('accounts.urls')), # Inclui as outras URLs de 'accounts'
]
