from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-2fa/', views.verify_2fa_view, name='verify_2fa'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('setup-2fa/', views.setup_2fa_view, name='setup_2fa'),
    path('disable-2fa/', views.disable_2fa_view, name='disable_2fa'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:pk>/edit/', views.user_update_view, name='user_update'),
    path(
        'users/<int:pk>/delete/',
        views.user_delete_view,
        name='user_delete'
    ),
    path(
        'password-reset/',
        views.password_reset_request_view,
        name='password_reset_request'
    ),
    path(
        'password-reset/<str:token>/',
        views.password_reset_confirm_view,
        name='password_reset_confirm'
    ),
]
