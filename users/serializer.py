from rest_framework import serializers
from users.models import MyUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField
    password = serializers.CharField
