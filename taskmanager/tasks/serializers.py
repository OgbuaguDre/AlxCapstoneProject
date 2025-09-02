from rest_framework import serializers
from django.utils import timezone
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        id = serializers.IntegerField(read_only=True)
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status',
                  'completed_at', 'created_at', 'updated_at', 'owner']

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

