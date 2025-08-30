from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

# your_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a task to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed only to the owner
        return obj.owner == request.user

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Prevent error during Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Set the owner as the logged-in user
        serializer.save(owner=self.request.user)

class RecentCompletedTasksView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if getattr(self, 'swagger_fake_view', False):
            return Response([])  # empty list during Swagger introspection

        seven_days_ago = timezone.now() - timedelta(days=7)
        tasks = Task.objects.filter(
            owner=request.user,
            status='completed',
            updated_at__gte=seven_days_ago
        ).order_by('-updated_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)