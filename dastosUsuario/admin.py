from django.contrib import admin
from dastosUsuario.models import Datos

# Register your models here.

class DatosAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario', 'avatar', 'whatsapp','identification',
                       'Shipping_Address', 'created', 'updated')

admin.site.register(Datos, DatosAdmin)