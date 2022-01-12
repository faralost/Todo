from django.contrib import admin

from todolistapp.models import Task, Status, Type


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'type', 'status']
    list_filter = ['status', 'type', 'status']
    search_fields = ['task']
    fields = ['task', 'description', 'type', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Type)
