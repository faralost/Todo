from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView

from todolistapp.forms import TaskForm, SimpleSearchForm
from todolistapp.models import Task, Project


class TaskIndexView(ListView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(task__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by('-created_at')

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['form'] = SimpleSearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def post(self, request, *args, **kwargs):
        tasks_id = request.POST.getlist('tasks_id')
        for id in tasks_id:
            task = Task.objects.get(pk=id)
            task.delete()
        return redirect('task_index')


class TaskView(DetailView):
    template_name = 'task/detail_view.html'
    model = Task


class TaskCreate(CreateView):
    form_class = TaskForm
    template_name = 'task/create.html'
    model = Task

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)


class TaskDelete(DeleteView):
    model = Task

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.project.pk})


class TaskUpdate(UpdateView):
    form_class = TaskForm
    template_name = 'task/update.html'
    model = Task

