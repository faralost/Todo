from django.urls import path

from todolistapp.views.task_views import IndexView, TaskView, TaskCreate, TaskDelete, TaskUpdate

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('tasks/add/', TaskCreate.as_view(), name='task_add'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/<int:pk>/update/', TaskUpdate.as_view(), name='task_update'),
]
