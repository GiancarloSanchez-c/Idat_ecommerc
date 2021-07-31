from django.urls import path
from .views import RegisterView, EmailVerifyView, LoginView, LogoutView, ResetPasswordView, ResetPasswordCheckView, PasswordChangeView 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify/', EmailVerifyView.as_view(), name='email_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password_email/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password/<uidb64>/<token>', ResetPasswordCheckView.as_view(), name='reset_password_check'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
]
