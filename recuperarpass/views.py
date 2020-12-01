import coreapi
import time
import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

from rest_framework import parsers, renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.schemas import AutoSchema

from recuperarpass.serializers import *
from recuperarpass.models import ResetPasswordToken
from recuperarpass.signals import reset_password_token_created, pre_password_reset, post_password_reset
from recuperarpass.utils import get_client_masked_ip
from django.dispatch import receiver
from recuperarpass.signals import reset_password_token_created
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

User = get_user_model()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    # enviar un correo electrónico al usuario
    context = {
        'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        # ToDo: La URL puede (y debe) construirse utilizando el método `reverse` incorporado en python.
        'reset_password_url': "http://localhost:4200/nuevopass/?token={token}".format(token=reset_password_token.key)
    }

    # renderizar texto de correo electrónico
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # título:
        ("Solicitud para restablecer contraseña {title}".format(title="Conecta con ingeniería")),
        # mensaje:
        email_plaintext_message,
        # de:
        "noreply@somehost.local",
        # a:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

def get_password_reset_token_expiry_time(is_long_token=False):
    """
    Devuelve el tiempo de caducidad del token de restablecimiento de contraseña en horas (predeterminado: 24) Establezca Django SETTINGS.DJANGO REST_MULTITOKENAUTH_RESET_TOKEN EXPIRY_TIME para sobrescribir este tiempo: return: tiempo de caducidad
    """

    if is_long_token:
        return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_LONG_EXPIRY_TIME', 48)

    # obtener tiempo de validación de token
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_use_username():
    """
  #  Returns if user search need to be based on username instead of email
   # Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_USE_USERNAME to overwrite this
    #:return: use username
    #"""
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_USE_USERNAME', False)


def get_new_token(user, request):
    """
    Devolver nuevo token de restablecimiento de contraseña
    """
    return ResetPasswordToken.objects.create(
        user=user,
        user_agent=request.META['HTTP_USER_AGENT'],
        ip_address=get_client_masked_ip(request)
    )


def filter_parameters_from_token(token_input):
    if token_input and '?' in token_input:
        token_input = token_input.split('?')[0]

    return token_input


class ResetPasswordConfirm(APIView):
    """
    Una vista Api que proporciona un método para restablecer una contraseña basada en un token único
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = PasswordTokenSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('password', location='body', required=True),
            coreapi.Field('token', location='body', required=True),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = filter_parameters_from_token(serializer.validated_data['token'])

        # obtener tiempo de validación de token

        # encontrar token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'error': 'token not found'}, status=status.HTTP_404_NOT_FOUND)

        if reset_password_token.expired:
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        if reset_password_token.used:
            return Response({'error': 'token used'}, status=status.HTTP_400_BAD_REQUEST)

        password_reset_token_validation_time = get_password_reset_token_expiry_time(
            is_long_token=reset_password_token.is_long_token
        )

        # comprobar fecha de caducidad
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            # marca de token como caducada
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_password_token.user.is_active:
            return Response({'error': 'inactive user'}, status=status.HTTP_400_BAD_REQUEST)

        # cambiar contraseña de usuario
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user, request=request)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user, request=request)

        # Marcar token como se usa
        ResetPasswordToken.objects.filter(user=reset_password_token.user).update(used=True)

        return Response()


class ResetPasswordCheck(APIView):
    """
    Una vista Api que proporciona un método para verificar que un token sea válido.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = TokenSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('token', location='body', required=True),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = filter_parameters_from_token(serializer.validated_data['token'])

        # encontrar token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'error': 'token not found'}, status=status.HTTP_404_NOT_FOUND)

        if reset_password_token.expired:
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        if reset_password_token.used:
            return Response({'error': 'token used'}, status=status.HTTP_400_BAD_REQUEST)

        password_reset_token_validation_time = get_password_reset_token_expiry_time(
            is_long_token=reset_password_token.is_long_token
        )

        # comprobar fecha de caducidad
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # marca token como caducada
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_password_token.user.is_active:
            return Response({'error': 'inactive user'}, status=status.HTTP_400_BAD_REQUEST)

        return Response()


class ResetPasswordRequestToken(APIView):
    """
    Una vista Api que proporciona un método para solicitar un token de restablecimiento de contraseña basado en una dirección de correo electrónico
    Envía una señal reset_password_token_created cuando se creó un token de reinicio
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = EmailSerializer

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('email', location='body', required=True, type='email'),
        ]
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # encontrar un usuario por dirección de correo electrónico (búsqueda sin distinción entre mayúsculas y minúsculas)
        if get_use_username():
            users = User.objects.filter(username__iexact=email)
        else:    
            users = User.objects.filter(email__iexact=email)

        active_user_found = False

        # iterar sobre todos los usuarios y verificar si hay algún usuario que esté activo
        # también verifique si la contraseña se puede cambiar (es utilizable), ya que podría haber usuarios que no están permitidos
        # para cambiar su contraseña (por ejemplo, usuario LDAP)
        for user in users:
            if user.is_active and user.has_usable_password():
                active_user_found = True

        # No se ha encontrado ningún usuario activo, genera un error de validación
        if not active_user_found:
            time.sleep(random.randint(500, 2000) / 1000)
            return Response()

        # por último pero no menos importante: iterar sobre todos los usuarios que están activos y pueden cambiar su contraseña
        # y crea un token de restablecimiento de contraseña y envía una señal con el token creado
        for user in users:
            if user.is_active and user.has_usable_password():
                # define el token como ninguno por ahora
                token = None

                # comprobar si la usuario ya tiene un token
                if user.password_reset_tokens.filter(expired=False, used=False).count() > 0:
                    # sí, ya tiene un token, reutilice este token
                    token = user.password_reset_tokens.all()[0]

                   # obtener tiempo de validación de token
                    password_reset_token_validation_time = get_password_reset_token_expiry_time(
                        is_long_token=token.is_long_token
                    )

                    expiry_date = token.created_at + timedelta(
                        hours=password_reset_token_validation_time)

                    if timezone.now() > expiry_date:
                        token.expired = True
                        token.used = True
                        token.save()
                        token = get_new_token(user, request)

                else:
                    # no hay token, genera un nuevo token
                    token = get_new_token(user, request)
                # envía una señal de que se creó el token de contraseña
                # deje que quien reciba esta señal se encargue de enviar el correo electrónico para restablecer la contraseñ
                reset_password_token_created.send(
                    sender=self.__class__,
                    reset_password_token=token,
                    request=request
                )
        # hecho
        return Response()


reset_password_confirm = ResetPasswordConfirm.as_view()
reset_password_check = ResetPasswordCheck.as_view()
reset_password_request_token = ResetPasswordRequestToken.as_view()