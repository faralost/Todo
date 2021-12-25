from django.urls import path

from todolistapp.views import index_view, tasks_list_view, task_view, task_create, task_delete

urlpatterns = [
    path('', index_view),
    path('tasks/', tasks_list_view),
    path('task/<int:pk>/', task_view),
    path('tasks/add/', task_create),
    path('task/delete', task_delete)
]
