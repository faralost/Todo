from django.contrib import admin

from todolistapp.models import Task, Status, Type


class MembershipInline(admin.TabularInline):
    model = Task.types.through


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'created_at']
    list_filter = ['status', 'types']
    search_fields = ['task']
    fields = ['task', 'description', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [
        MembershipInline,
    ]
    exclude = ('types',)


class TypeAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Type, TypeAdmin)
