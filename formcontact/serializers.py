from rest_framework import serializers

class ContactSerailizer(serializers.Serializer):
    subject = serializers.CharField()
    from_email = serializers.EmailField()
    message = serializers.CharField()