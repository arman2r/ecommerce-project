from django.urls import path
from recuperarpass.views import reset_password_request_token, reset_password_confirm, reset_password_check

app_name = 'password_reset'

urlpatterns = [
    path('confirm/', reset_password_confirm, name="reset-password-confirm"),
    path('check/', reset_password_check, name="reset-password-check"),
    path('', reset_password_request_token, name="reset-password-request"),
]