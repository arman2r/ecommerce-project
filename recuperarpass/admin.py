from django.contrib import admin
from recuperarpass.models import ResetPasswordToken

# Register your models here.

@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'used', 'expired', 'ip_address', 'user_agent')