from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todolistapp.forms import ProjectForm, ProjectDeleteForm
from todolistapp.models import Project, Task


class ProjectIndexView(ListView):
    model = Project
    template_name = 'project/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_end')


class ProjectView(DetailView):
    template_name = 'project/detail_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        project_tasks = Paginator(self.object.tasks.all().order_by('-created_at'), 5)
        context['project_tasks'] = project_tasks.get_page(page)
        context['page_obj'] = project_tasks.get_page(page)
        context['is_paginated'] = project_tasks.get_page(page)
        return context


class ProjectCreate(CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdate(UpdateView):
    template_name = 'project/update.html'
    form_class = ProjectForm
    model = Project


class ProjectDelete(DeleteView):
    template_name = 'project/delete.html'
    model = Project
    success_url = reverse_lazy('project_index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.method == "POST":
            self.object_form = ProjectDeleteForm(instance=self.get_object(), data=self.request.POST)
        else:
            self.object_form = ProjectDeleteForm()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.object_form
        return context

    def post(self, request, *args, **kwargs):
        if self.object_form.is_valid():
            return super().delete(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
