from django.contrib import admin

from todolistapp.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'deadline', 'task_description']
    list_filter = ['status']
    search_fields = ['task']
    fields = ['task', 'status', 'deadline', 'task_description']


admin.site.register(Task, TaskAdmin)
