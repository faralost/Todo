from django.contrib import admin

from todolistapp.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'deadline']
    list_filter = ['status']
    search_fields = ['task']
    fields = ['task', 'status', 'deadline']


admin.site.register(Task, TaskAdmin)
