from django.shortcuts import render
from rest_framework.views import  APIView
from .serializer import LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class LoginAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email = email, password=password)

                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid password',
                        'data': {}
                    })
                refresh = RefreshToken.for_user(user)

                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
