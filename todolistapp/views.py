from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from todolistapp.forms import TaskForm
from todolistapp.models import Task


def index_view(request):
    return render(request, 'index.html')


def tasks_list_view(request):
    tasks = Task.objects.order_by('-pk')
    return render(request, 'tasks.html', {'tasks': tasks})


def task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_view.html', {'task': task})


def task_create(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = request.POST.get('task').strip()
            status = request.POST.get('status')
            deadline = request.POST.get('deadline')
            task_description = request.POST.get('task_description')
            new_task = Task.objects.create(task=task, status=status, deadline=deadline or None,
                                           task_description=task_description or None)
            return redirect('task_view', pk=new_task.pk)
        return render(request, 'task_create.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', {'task': task})
    elif request.method == 'POST':
        task.delete()
        return redirect('tasks_list_view')


def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        return render(request, 'update.html', {'task': task, 'status_choices': Task.status_choices})
    elif request.method == 'POST':
        task.task = request.POST.get('task')
        task.status = request.POST.get('status')
        task.deadline = request.POST.get('deadline') or None
        task.task_description = request.POST.get('task_description') or None
        task.save()
        return redirect('task_view', pk=task.pk)
