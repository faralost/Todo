from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from todolistapp.models import Task


def index_view(request):
    return render(request, 'index.html')


def tasks_list_view(request):
    tasks = Task.objects.order_by('deadline')
    return render(request, 'tasks.html', {'tasks': tasks})


def task_view(request):
    task_pk = request.GET.get('pk')
    task = Task.objects.get(pk=task_pk)
    context = {'task': task}
    return render(request, 'task_view.html', context)


def task_create(request):
    if request.method == 'GET':
        return render(request, 'task_create.html', {'status_choices': Task.status_choices})
    else:
        try:
            task = request.POST.get('task').strip()
            if not task:
                response = redirect('/tasks/add/')
                return response
            status = request.POST.get('status')
            deadline = request.POST.get('deadline')
            new_task = Task.objects.create(task=task, status=status, deadline=deadline or None)
            return HttpResponseRedirect(f'/task?pk={new_task.pk}')
        except ValidationError:
            response = redirect('/tasks/add/')
            return response


def task_delete(request):
    task_pk = request.GET.get('pk')
    task = Task.objects.get(pk=task_pk)
    task.delete()
    response = redirect('/tasks/')
    return response
