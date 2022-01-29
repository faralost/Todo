from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from todolistapp.forms import ProjectForm
from todolistapp.models import Project


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


class ProjectCreate(CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})
