from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Task

class AuthTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {"username": "john", "email": "john@example.com", "password": "Password123!", "password2": "Password123!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        user = User.objects.create_user(username="john", password="Password123!")
        url = reverse('login')
        response = self.client.post(url, {"username": "john", "password": "Password123!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="Password123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_task(self):
        url = reverse('task-list')
        data = {"title": "Test Task", "description": "My task", "priority": "Medium"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_list_tasks(self):
        Task.objects.create(title="Task 1", owner=self.user, priority="Low")
        Task.objects.create(title="Task 2", owner=self.user, priority="High")
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        task = Task.objects.create(title="Old Task", owner=self.user, priority="Low")
        url = reverse('task-detail', args=[task.id])
        response = self.client.patch(url, {"title": "Updated Task"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task")

    def test_delete_task(self):
        task = Task.objects.create(title="Task to delete", owner=self.user, priority="Low")
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_mark_complete_and_incomplete(self):
        task = Task.objects.create(title="Complete Me", owner=self.user, priority="High")
        url_complete = reverse('task-complete', args=[task.id])
        url_incomplete = reverse('task-incomplete', args=[task.id])

        response = self.client.patch(url_complete)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, "Completed")

        response = self.client.patch(url_incomplete)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, "Pending")
