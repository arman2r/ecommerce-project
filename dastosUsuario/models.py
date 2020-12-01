from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Datos(models.Model):
    usuario = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name ="Avatar", upload_to='dastosUsuario', height_field=None, width_field=None, max_length=None)
    whatsapp = models.CharField(verbose_name ="Whatsapp", blank=False, null=False, max_length=12)
    identification = models.CharField(verbose_name="C.C o Nit", blank=True, null=True, max_length=50)
    Shipping_Address = models.CharField(verbose_name="Dirección de envio", max_length=50, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')
    
    class Meta:
        verbose_name = "Dato"
        verbose_name_plural = "Datos"
        ordering = ['-created']
        
    def __str__(self):
        return self.Shipping_Address
    
