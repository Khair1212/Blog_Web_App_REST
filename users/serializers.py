from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User, OTP
from .utils import Util


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'email')


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validating password 1 and password2
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
        # password = validate_data.pop('password', None)
        # instance = self.Meta.model(**validate_data)
        # if password is not None:
        #     instance.set_password(password)
        # instance.save()
        # return instance


class AccountActiveSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10)

    class Meta:
        fields = ['otp']

    def validate(self, attrs):
        otp = attrs.get('otp')
        umail = self.context.get('umail')
        email = smart_str(urlsafe_base64_decode(umail))
        print()
        user = User.objects.get(email=email)
        otp_obj = OTP.objects.get(user=user)
        if OTP.objects.filter(code=otp).exists():
            otp_obj.has_used = True
            otp_obj.save()
            return attrs
        else:
            ValidationError('Your OTP is not correct')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token", token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            print("Password Reset Link", link)

            # Send Email
            body = 'Click the following link to reset your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }

            Util.send_email(data)

            return attrs
        else:
            raise ValidationError('You are not a Registered User')


class PasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
