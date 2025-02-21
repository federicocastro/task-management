from django.test import TestCase

from ..models import Task
from ..serializers import TaskSerializer


class TaskSerializerTest(TestCase):
    def setUp(self):
        """Crear una tarea para los tests"""
        self.task = Task.objects.create(title="Test Task", description="Testing serializer", completed=False)

    def test_serialize_task(self):
        serializer = TaskSerializer(instance=self.task)
        expected_data = {
            "id": self.task.id,
            "title": "Test Task",
            "description": "Testing serializer",
            "completed": False,
            "created": self.task.created.isoformat().replace("+00:00", "Z"),
            "modified": self.task.modified.isoformat().replace("+00:00", "Z"),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_deserialize_valid_data(self):
        data = {
            "title": "New Task",
            "description": "New Task Description",
            "completed": True
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.description, "New Task Description")
        self.assertTrue(task.completed)

    def test_deserialize_invalid_data_missing_title(self):
        data = {
            "description": "Missing title",
            "completed": False
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_deserialize_invalid_title_length(self):
        data = {
            "title": "T" * 256,
            "description": "Title too long",
            "completed": False
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_deserialize_invalid_completed_type(self):
        data = {
            "title": "Invalid Completed",
            "description": "Should fail",
            "completed": "not_a_boolean"
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("completed", serializer.errors)
