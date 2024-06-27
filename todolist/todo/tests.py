from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task


class TaskTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Test Task', description='Test Description', user=self.user,
                                        completed=False)

    def test_task_list_view(self):
        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'templates/task_list.html')
        self.assertContains(response, self.task.title)

    def test_task_detail_view(self):
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '/todo/task.html')
        self.assertContains(response, self.task.title)

    def test_task_create_view(self):
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'New Description',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        response = self.client.post(reverse('task-update', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'completed': True
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.completed, True)

    def test_task_delete_view(self):
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful delete
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_view(self):
        User.objects.create_user(username='testuser', password='testpass')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

# Remember to adjust 'reverse' arguments to match your actual URL patterns and names.
