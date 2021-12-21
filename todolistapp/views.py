from django.shortcuts import render

from todolistapp.models import Task


def index_view(request):
    return render(request, 'index.html')


def tasks_list_view(request):
    tasks = Task.objects.order_by('deadline')
    return render(request, 'tasks.html', {'tasks': tasks})
