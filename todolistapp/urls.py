from django.urls import path

from todolistapp.views.project_views import ProjectIndexView
from todolistapp.views.task_views import TaskIndexView, TaskView, TaskCreate, TaskDelete, TaskUpdate

urlpatterns = [
    path('', TaskIndexView.as_view(), name='task_index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('tasks/add/', TaskCreate.as_view(), name='task_add'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('projects/', ProjectIndexView.as_view(), name='project_index'),
]
