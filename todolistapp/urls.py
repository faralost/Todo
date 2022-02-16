from django.urls import path

from todolistapp.views.project_views import ProjectIndexView, ProjectView, ProjectCreate, ProjectUpdate, ProjectDelete, \
    ProjectChangeUser
from todolistapp.views.task_views import TaskIndexView, TaskView, TaskCreate, TaskDelete, TaskUpdate

app_name = 'todolistapp'

urlpatterns = [
    path('', ProjectIndexView.as_view(), name='project_index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
    path('tasks/', TaskIndexView.as_view(), name='task_index'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('projects/add/', ProjectCreate.as_view(), name='project_add'),
    path('project/<int:pk>/tasks/add/', TaskCreate.as_view(), name='project_task_add'),
    path('project/<int:pk>/update/', ProjectUpdate.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
    path('project/<int:pk>/change-users/', ProjectChangeUser.as_view(), name='project_change_user'),
]