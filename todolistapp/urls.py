from django.urls import path

from todolistapp.views import task_update_view, IndexView, TaskView, TaskCreate, TaskDelete

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('tasks/add/', TaskCreate.as_view(), name='task_add'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('task/<int:pk>/update/', task_update_view, name='task_update'),
]
