from django.urls import path

from todolistapp.views import index_view, tasks_list_view, task_view, task_create, task_delete, task_update_view

urlpatterns = [
    path('', index_view, name='index'),
    path('tasks/', tasks_list_view, name='tasks_list_view'),
    path('task/<int:pk>/', task_view, name='task_view'),
    path('tasks/add/', task_create, name='task_add'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    path('task/<int:pk>/update/', task_update_view, name='task_update'),
]
