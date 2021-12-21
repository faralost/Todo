from django.urls import path

from todolistapp.views import index_view, tasks_list_view, task_view

urlpatterns = [
    path('', index_view),
    path('tasks/', tasks_list_view),
    path('task/', task_view),
]
