from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer
class SignupView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        ser=SignupSerializer(data=request.data)
        if ser.is_valid():
            user=ser.save(); refresh=RefreshToken.for_user(user)
            return Response({'access':str(refresh.access_token),'refresh':str(refresh)}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        u=request.data.get('username'); p=request.data.get('password')
        user=authenticate(username=u,password=p)
        if not user: return Response({'detail':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh=RefreshToken.for_user(user); return Response({'access':str(refresh.access_token),'refresh':str(refresh)})
