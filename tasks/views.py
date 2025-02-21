from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
