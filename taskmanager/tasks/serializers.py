from rest_framework import serializers
from django.utils import timezone
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = [
            "id", "owner", "title", "description", "due_date",
            "priority", "status", "completed_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["status", "completed_at", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def update(self, instance, validated_data):
        # Block edits when completed unless status explicitly reverted via dedicated endpoint
        if instance.status == Task.Status.COMPLETED:
            raise serializers.ValidationError(
                "Completed tasks cannot be edited. Revert to incomplete first."
            )
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # confirm password

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
