from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from todolistapp.forms import TaskForm
from todolistapp.models import Task, Project
from todolistapp.views.base import SearchListView


class TaskIndexView(SearchListView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = ['-created_at']
    search_fields = ['task__icontains', 'description__icontains']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False)

    def post(self, request, *args, **kwargs):
        tasks_id = request.POST.getlist('tasks_id')
        for id in tasks_id:
            task = Task.objects.get(pk=id)
            task.soft_delete()
        return redirect('todolistapp:task_index')


class TaskView(DetailView):
    template_name = 'task/detail_view.html'
    model = Task

    def get_object(self, queryset=None):
        task = super(TaskView, self).get_object()
        if task.is_deleted:
            raise Http404
        return task


class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'task/create.html'
    model = Task

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)


class TaskDelete(DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('todolistapp:project_view', kwargs={'pk': self.object.project.pk})


class TaskUpdate(UpdateView):
    form_class = TaskForm
    template_name = 'task/update.html'
    model = Task

