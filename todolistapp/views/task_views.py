from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from todolistapp.forms import TaskForm
from todolistapp.models import Task, Project
from todolistapp.views.base import SearchListView


class TaskIndexView(LoginRequiredMixin, SearchListView):
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
        if not self.request.user.has_perm('todolistapp.delete_task'):
            raise PermissionDenied
        tasks_id = request.POST.getlist('tasks_id')
        for id in tasks_id:
            task = Task.objects.get(pk=id)
            task.soft_delete()
        return redirect('todolistapp:task_index')


class TaskView(LoginRequiredMixin, DetailView):
    template_name = 'task/detail_view.html'
    model = Task

    def get_object(self, queryset=None):
        task = super(TaskView, self).get_object()
        if task.is_deleted:
            raise Http404
        return task


class TaskCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'todolistapp.add_task'
    form_class = TaskForm
    template_name = 'task/create.html'
    model = Task

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        return super().has_permission() and self.request.user in project.users.all() or self.request.user.is_superuser

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)


class TaskDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'todolistapp.delete_task'
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('todolistapp:project_view', kwargs={'pk': self.object.project.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()


class TaskUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'todolistapp.change_task'
    form_class = TaskForm
    template_name = 'task/update.html'
    model = Task

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()
