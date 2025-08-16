from rest_framework import serializers
from django.utils import timezone
from .models import Task

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
