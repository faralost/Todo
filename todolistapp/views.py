from django.shortcuts import render

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
        return render(request, 'task_create.html')
    else:
        task = request.POST.get('task')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline')
        new_task = Task.objects.create(task=task, status=status, deadline=deadline or None)
        context = {"task": new_task}

        return render(request, 'task_view.html', context)
