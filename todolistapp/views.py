from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from todolistapp.forms import TaskForm
from todolistapp.models import Task


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.order_by('-pk')
        return context

    # def post(self, request, *args, **kwargs):
    #     tasks_id = request.POST.getlist('tasks_id')
    #     for id in tasks_id:
    #         task = Task.objects.get(pk=id)
    #         task.delete()
    #     return redirect('index')


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return super().get_context_data(**kwargs)


class TaskCreate(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})

    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect('task_view', pk=new_task.pk)
        return render(request, 'task_create.html', {'form': form})


class TaskDelete(View):
    def get(self, request, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return render(request, 'delete.html', {'task': task})

    def post(self, request, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect('index')


class TaskUpdate(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        deadline = task.deadline.strftime('%Y-%m-%d') if task.deadline else task.deadline
        form = TaskForm(initial={
            'task': task.task,
            'status': task.status,
            'deadline': deadline,
            'task_description': task.task_description
        })
        return render(request, 'update.html', {'task': task, 'form': form})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.task = form.cleaned_data.get('task')
            task.status = form.cleaned_data.get('status')
            task.deadline = form.cleaned_data.get('deadline') or None
            task.task_description = form.cleaned_data.get('task_description') or None
            task.save()
            return redirect('task_view', pk=task.pk)
        return render(request, 'update.html', {'task': task, 'form': form})
