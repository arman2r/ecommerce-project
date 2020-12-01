from django.core.mail import BadHeaderError, message, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import  APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from usuario.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class ContactView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, *args, **kwargs):
        subject = request.data.get('subject')
        name = request.data.get('name')
        message = request.data.get('message')
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        body = render_to_string(
            'content.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'message': message,
            },
        )

        email_message = EmailMessage(
            subject='Mensaje de usuario',
            body=body,
            from_email=email,
            to=[EMAIL_HOST_USER],
        )
        email_message.content_subtype = 'html'
        email_message.send()
        
        
        return Response({"success": "Sent"})
        #return Response({'success': "Failed"}, status=status.HTTP_400_BAD_REQUEST)








"""from django.shortcuts import render
from rest_framework.views import  APIView
from rest_framework.permissions import AllowAny
from formcontact.serializers import ContactSerailizer
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail



# Create your views here.

class ContactView(APIView):

    def post(self, request, *args, **kwargs):
         serailizer = ContactSerailizer(request.data)
         if serailizer.is_valid():
             data = serailizer.validated_data
             email = validated_data.get('email')
             name = validated_data.get('name')
             message = validated_data.get('name')
             send_mail(
                'Sent email from {}'.format(name),
                'Here is the message. {}'.format(validate_data.get('message')),
                email,
                ['ancizar.rubio@gmail.com.com'],
                fail_silently=False,
            )
             
             return Response({"success": "Sent"})
             return Response({'success': "Failed"}, status=status.HTTP_400_BAD_REQUEST)"""
            
        
        