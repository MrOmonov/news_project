from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetCompleteView, PasswordResetConfirmView)
from django.shortcuts import redirect
from django.urls import path, reverse_lazy

from users.views import (loginView, profile_view,
                         register_view, RegisterView,
                         profile_edit)

urlpatterns = [
    # path('login/', LoginView, name="login_user")
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login_user'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout_user'),
    path('profile/', profile_view, name='profile_user'),
    path('profile/edit', profile_edit, name='profile_edit'),
    path('password_change/', PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      email_template_name='users/email_template.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    # path('registration/', register_view, name='registration'),
    path('registration/', RegisterView.as_view(), name='registration'),

]