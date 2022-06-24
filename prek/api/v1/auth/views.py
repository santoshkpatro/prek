from django.conf import settings
import jwt
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from prek.models.user import User
from .serializers import LoginSerializer, RegisterSerializer
from .helpers import send_verification_email


@api_view(['POST'])
def register_view(request):
    register_serializer = RegisterSerializer(data=request.data)

    if not register_serializer.is_valid():
        return Response(data={'detail': 'Invalid data input', 'errors': register_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    new_user_credentials = register_serializer.data
    email = new_user_credentials.get('email')
    try:
        existing_user = User.objects.get(email=email)

        if not existing_user.is_email_verified:
            # Send verification email
            send_verification_email(existing_user.email)
            return Response(data={'detail': 'Email verification link has been sent'}, status=status.HTTP_200_OK)

        return Response(data={'detail': 'Account exists with this email address'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        password = new_user_credentials.pop('password')
        user = User(**new_user_credentials)
        user.set_password(password)
        user.is_email_verified = False
        user.save()

        # Send verification email
        send_verification_email(user.email)

        return Response(data={'detail': 'Account created successfully!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    login_serializer = LoginSerializer(data=request.data)

    if not login_serializer.is_valid():
        return Response(data={'detail': 'Invalid input details', 'errors': login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    email = login_serializer.data.get('email')

    try:
        user = User.active_objects.get(email=email)
        auth_user = authenticate(**login_serializer.data)

        if not user.is_email_verified:
            return Response(data={'detail': 'Please verify your email to continue'}, status=status.HTTP_401_UNAUTHORIZED)

        # IP Address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            login_ip = x_forwarded_for.split(',')[0]
        else:
            login_ip = request.META.get('REMOTE_ADDR')

        # Incalid credentials
        if not auth_user:
            user.login_failed_attempts += 1
            user.login_failed_attempt_ip = login_ip
            user.save()
            return Response(data={'detail': 'Invalid security credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.password_reset_required:
            return Response(data={'detail': 'Please reset your password to continue'}, status=status.HTTP_401_UNAUTHORIZED)

        user.login_count += 1
        user.last_login = timezone.now()
        user.last_login_ip = login_ip
        user.save()

        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))

        return Response(data={'detail': 'Login success', 'data': {
            'access_token': access_token,
            'refresh_token': refresh_token
        }}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={'detail': 'Unable to fetch account details'}, status=status.HTTP_400_BAD_REQUEST)


class Verification(APIView):
    def get(self, request):
        # verification_type = request.query_params.get('verification_type')
        verification_token = request.query_params.get('verification_token')

        try:
            decoded_data = jwt.decode(verification_token, settings.SECRET_KEY, algorithms=["HS256"])
            email = decoded_data.get('email')
            print(email)
            try:
                user = User.objects.get(email=email)
                user.is_email_verified = True
                user.save()
                return Response(data={'detail': 'Email verified'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={'detail': 'Unable to fetch account details'}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'Verification token has been expired'}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidTokenError:
            return Response(data={'detail': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
