from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import FilterSet, filters
from .models import Task
from .serializers import TaskSerializer, RegisterSerializer, UserSerializer
from .permissions import IsOwner
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView


class TaskFilter(FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    priority = filters.CharFilter(field_name="priority", lookup_expr="exact")
    due_date_before = filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="lte")
    due_date_after = filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Task
        fields = ["status", "priority", "due_date"]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    ordering_fields = ["due_date", "priority"]
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by("due_date")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.Status.COMPLETED:
            return Response({"detail": "Task already completed."}, status=400)
        task.mark_complete()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=["post"])
    def incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.Status.PENDING:
            return Response({"detail": "Task is already pending."}, status=400)
        task.mark_incomplete()
        task.save(update_fields=["status", "completed_at", "updated_at"])
        return Response(TaskSerializer(task).data)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout user
class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

