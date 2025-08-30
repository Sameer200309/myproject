from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create tasks
        Task.objects.create(owner=self.user, title='Task 1', status='completed')
        Task.objects.create(owner=self.user, title='Task 2', status='pending')
        Task.objects.create(owner=self.user, title='Task 3', status='completed')

        # Get JWT access token
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']

        # Include token in all requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    # Endpoint 1: Recent Completed Tasks
    def test_recent_completed_tasks(self):
        response = self.client.get('/api/recent-completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for task in response.data:
            self.assertEqual(task['status'], 'completed')

    # Endpoint 2: Create Task
    def test_create_task(self):
        data = {'title': 'New Task', 'status': 'pending'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    # Endpoint 3: Get Task List
    def test_get_task_list(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 3)
