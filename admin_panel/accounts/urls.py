from django.urls import path, include
from rest_auth.views import (
    LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView)
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    # path('register/', include('rest_auth.registration.urls')),
    path('refresh/', refresh_jwt_token, name="rest_jwt_refresh"),

]
