from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# class MeView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserSerializer

#     def get_object(self):
#         return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    """
    Admin-only CRUD for users.
    """
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
  
