from django.db import models
import binascii
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = _("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return binascii.hexlify(os.urandom(32)).decode()


    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='password_reset_tokens', on_delete=models.CASCADE, verbose_name=_("The User which is associated to this password reset token"))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_("When was this token generated"))

    # Key field, though it is not the primary key of the model
    key = models.CharField(_("Key"), max_length=64, db_index=True, unique=True)
    ip_address = models.GenericIPAddressField(_("The IP address of this session"), default="127.0.0.1")
    user_agent = models.CharField(max_length=256, verbose_name=_("HTTP User Agent"), default="")
    is_long_token = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)