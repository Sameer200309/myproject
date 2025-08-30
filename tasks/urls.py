from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, RecentCompletedTasksView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger schema view
swagger_schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version='v1',
        description="API documentation with JWT authentication",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router for your viewsets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('recent-completed/', RecentCompletedTasksView.as_view(), name='recent-completed'),
    path('swagger/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
