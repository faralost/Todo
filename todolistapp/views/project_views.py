from django.core.paginator import Paginator
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin

from todolistapp.forms import ProjectForm
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