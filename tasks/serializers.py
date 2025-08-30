from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
