from django.urls import path, include

# Классы обработчики аутентификации Django
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Определённые ранее обработчики
    # path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # Шаблоны для доступа к обработчикам смены пароля.
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # # Шаблоны востановления пороля
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
]

# PaasswordResetView – обработчик восстановления пароля. Он генерирует временную
# ссылку с токеном и отправляет ее на  электронную почту пользователя;
# PasswordResetDoneView – отображает страницу с сообщением о том, что ссылка
# восстановления пароля была отправлена на электронную почту;
# PasswordResetConfirmView – позволяет пользователю указать новый пароль;
# PasswordResetCompleteView – отображает сообщение об успешной смене пароля.
