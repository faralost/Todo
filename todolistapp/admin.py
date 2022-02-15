from django.contrib import admin

from todolistapp.models import Task, Status, Type, Project


class MembershipInline(admin.TabularInline):
    model = Task.types.through


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'created_at', 'project', 'is_deleted']
    list_editable = ['is_deleted']
    list_filter = ['status', 'types', 'project']
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


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_start', 'date_end']
    search_fields = ['name']
    fields = ['name', 'description', 'date_start', 'date_end', 'users']
    filter_horizontal = ['users']


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Type, TypeAdmin)
admin.site.register(Project, ProjectAdmin)
