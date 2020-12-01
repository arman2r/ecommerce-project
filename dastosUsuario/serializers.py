from rest_framework import serializers
from dastosUsuario.models import Datos


class DatosSerializer(serializers.ModelSerializer):
     class Meta:
        model = Datos
        fields = ['id','usuario', 'avatar', 'whatsapp', 'identification', 'Shipping_Address']