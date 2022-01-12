from django.shortcuts import render, redirect, get_object_or_404

from todolistapp.forms import TaskForm
from todolistapp.models import Task


def index_view(request):
    return render(request, 'index.html')


def tasks_list_view(request):
    if request.method == 'GET':
        tasks = Task.objects.order_by('-pk')
        return render(request, 'tasks.html', {'tasks': tasks})
    else:
        tasks_id = request.POST.getlist('tasks_id')
        for id in tasks_id:
            task = Task.objects.get(pk=id)
            task.delete()
        return redirect('tasks_list_view')


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
            task = form.cleaned_data.get('task')
            status = form.cleaned_data.get('status')
            deadline = form.cleaned_data.get('deadline')
            task_description = form.cleaned_data.get('task_description')
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
        deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else task.deadline
        form = TaskForm(initial={
            'task': task.task,
            'status': task.status,
            'deadline': deadline,
            'task_description': task.task_description
        })
        return render(request, 'update.html', {'task': task, 'form': form})
    elif request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.task = form.cleaned_data.get('task')
            task.status = form.cleaned_data.get('status')
            task.deadline = form.cleaned_data.get('deadline') or None
            task.task_description = form.cleaned_data.get('task_description') or None
            task.save()
            return redirect('task_view', pk=task.pk)
        return render(request, 'update.html', {'task': task, 'form': form})

