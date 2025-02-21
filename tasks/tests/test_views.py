from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.task_completed = Task.objects.create(title="Completed Task", description="Test", completed=True)
        self.task_pending = Task.objects.create(title="Pending Task", description="Test", completed=False)
        self.list_create_url = reverse("task-list-create")

    def test_get_task_list(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_completed_tasks(self):
        response = self.client.get(self.list_create_url, {"completed": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["completed"])

    def test_get_pending_tasks(self):
        response = self.client.get(self.list_create_url, {"completed": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertFalse(response.data[0]["completed"])

    def test_create_task(self):
        data = {"title": "New Task", "description": "New Task Description", "completed": False}
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.last().title, "New Task")

    def test_create_task_without_title(self):
        data = {"description": "Task without title", "completed": False}
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_get_task_detail(self):
        detail_url = reverse("task-detail", kwargs={"pk": self.task_pending.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task_pending.title)

    def test_update_task(self):
        detail_url = reverse("task-detail", kwargs={"pk": self.task_pending.pk})
        data = {"title": "Updated Task", "description": "Updated Description", "completed": True}
        response = self.client.put(detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_pending.refresh_from_db()
        self.assertEqual(self.task_pending.title, "Updated Task")
        self.assertTrue(self.task_pending.completed)

    def test_partial_update_task(self):
        detail_url = reverse("task-detail", kwargs={"pk": self.task_pending.pk})
        data = {"completed": True}
        response = self.client.patch(detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_pending.refresh_from_db()
        self.assertTrue(self.task_pending.completed)

    def test_delete_task(self):
        detail_url = reverse("task-detail", kwargs={"pk": self.task_pending.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)  # Solo queda la completada

    def test_delete_non_existent_task(self):
        response = self.client.delete(reverse("task-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
