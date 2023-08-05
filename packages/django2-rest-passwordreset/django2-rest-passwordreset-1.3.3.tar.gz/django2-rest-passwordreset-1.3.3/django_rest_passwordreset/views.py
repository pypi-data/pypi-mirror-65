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

from django_rest_passwordreset.serializers import *
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset
from django_rest_passwordreset.utils import get_client_masked_ip

User = get_user_model()


def get_password_reset_token_expiry_time(is_long_token=False):
    """
    Returns the password reset token expirty time in hours (default: 24)
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME to overwrite this time
    :return: expiry time
    """

    if is_long_token:
        return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_LONG_EXPIRY_TIME', 48)

    # get token validation time
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_use_username():
    """
    Returns if user search need to be based on username instead of email
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_USE_USERNAME to overwrite this
    :return: use username
    """
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_USE_USERNAME', False)


def get_new_token(user, request):
    """
    Return new reset password token
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
    An Api View which provides a method to reset a password based on a unique token
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

        # get token validation time

        # find token
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

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            # mark token as expired
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_password_token.user.is_active:
            return Response({'error': 'inactive user'}, status=status.HTTP_400_BAD_REQUEST)

        # change users password
        if reset_password_token.user.has_usable_password():
            pre_password_reset.send(sender=self.__class__, user=reset_password_token.user, request=request)
            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(sender=self.__class__, user=reset_password_token.user, request=request)

        # Mark token as used
        ResetPasswordToken.objects.filter(user=reset_password_token.user).update(used=True)

        return Response()


class ResetPasswordCheck(APIView):
    """
    An Api View which provides a method to check that a token is valid.
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

        # find token
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

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # mark token as expired
            reset_password_token.expired = True
            reset_password_token.used = True
            reset_password_token.save()
            return Response({'error': 'token expired'}, status=status.HTTP_400_BAD_REQUEST)

        return Response()


class ResetPasswordRequestToken(APIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
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

        # find a user by email address (case insensitive search)

        if get_use_username():
            users = User.objects.filter(username__iexact=email)
        else:
            users = User.objects.filter(email__iexact=email)

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.is_active and user.has_usable_password():
                active_user_found = True

        # No active user found, raise a validation error
        if not active_user_found:
            time.sleep(random.randint(500, 2000) / 1000)
            return Response()

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.is_active and user.has_usable_password():
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.filter(expired=False, used=False).count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]

                    # get token validation time
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
                    # no token exists, generate a new token
                    token = get_new_token(user, request)
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(
                    sender=self.__class__,
                    reset_password_token=token,
                    request=request
                )
        # done
        return Response()


reset_password_confirm = ResetPasswordConfirm.as_view()
reset_password_check = ResetPasswordCheck.as_view()
reset_password_request_token = ResetPasswordRequestToken.as_view()
