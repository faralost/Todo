from django.urls import path

from todolistapp.views import index_view, tasks_list_view

urlpatterns = [
    path('', index_view),
    path('tasks/', tasks_list_view),
]
