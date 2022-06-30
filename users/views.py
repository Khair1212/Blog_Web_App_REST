import random

from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView

from .email import send_otp_via_email
from .models import User, OTP
from .serializers import UserSerializer, RegisterUserSerializer, UpdateUserSerializer, ResetPasswordSerializer, \
    PasswordConfirmSerializer, AccountActiveSerializer
from django.contrib.auth import get_user_model
from .permissions import UserPermission
from .renderers import UserRenderer


# Create your views here.

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (UserPermission,)
    lookup_field = 'id'
    renderer_classes = [UserRenderer, ]
    default_serializer_class = UserSerializer
    serializer_classes = {
        'list': UserSerializer,
        'create': RegisterUserSerializer,
        'retrieve': UserSerializer,
        'update': UpdateUserSerializer,
        'partial_update': UpdateUserSerializer,
        'destroy': UserSerializer
    }

    # Get Serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    # Get Permissions for specific action
    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = [AllowAny, ]
    #     elif self.action == 'list':
    #         self.permission_classes = [IsAdminUser, ]
    #     else:
    #         self.permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in self.permission_classes]

    # override
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = RegisterUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                try:
                    serializer.save()


                    #  OTP Code Generation
                    user = User.objects.get(email=serializer.data.get('email'))
                    otp = random.randint(100000, 999999)
                    account_activation = OTP.objects.create(user=user, code=otp, task_type='active')
                    print(account_activation.code)

                    # link Generation
                    email = serializer.data.get('email')
                    umail = urlsafe_base64_encode(force_bytes(email))
                    link = 'http://127.0.0.1:8000/api/account_active/' + umail

                    # send_otp_via_email(user.email, account_activation)
                    return Response(
                        {'message': f'OTP has been sent to your email. Please verify your account by going to the following link: {link}'},
                        status=status.HTTP_201_CREATED)
                except Exception as e:
                    error = f'Server Error: {e}'
                    return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            return Response({'message': 'User has been deleted!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountActiveOrResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    def post(self, request, umail, format=None):
        try:
            serializer = AccountActiveSerializer(data=request.data, context={'umail': umail})
            try:
                if serializer.is_valid(raise_exception=True):
                    return Response({'message': 'Account Created Succesfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = f'Server Error: {e}'
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            try:
                if serializer.is_valid(raise_exception=True):
                    return Response({'message': 'Password Reset link has been send. Please check your Email'},
                                    status=status.HTTP_200_OK)

            except Exception as e:
                error = f'Server Error: {e}'
                return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordConfirmView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = (AllowAny,)

    def post(self, request, uid, token, format=None):
        serializer = PasswordConfirmSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
