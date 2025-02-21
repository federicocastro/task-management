from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completed', 'created', 'modified')
    list_filter = ('completed', 'created')
    search_fields = ('title', 'description')
    ordering = ('-created',)
