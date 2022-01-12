from django.urls import path

from todolistapp.views import task_create, task_delete, task_update_view, IndexView, TaskView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('tasks/add/', task_create, name='task_add'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    path('task/<int:pk>/update/', task_update_view, name='task_update'),
]
