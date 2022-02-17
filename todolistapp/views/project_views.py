from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todolistapp.forms import ProjectForm, ProjectDeleteForm, ProjectAddUserForm
from todolistapp.models import Project, Task


class ProjectIndexView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_end')


class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'project/detail_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        project_tasks = Paginator(self.object.tasks.all().filter(is_deleted=False).order_by('-created_at'), 5)
        context['project_tasks'] = project_tasks.get_page(page)
        context['page_obj'] = project_tasks.get_page(page)
        context['is_paginated'] = project_tasks.get_page(page)
        return context


class ProjectCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'todolistapp.add_project'
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project

    def form_valid(self, form):
        instance = form.save()
        instance.users.add(self.request.user)
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('todolistapp:project_view', kwargs={'pk': self.object.pk})


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'todolistapp.change_project'
    template_name = 'project/update.html'
    form_class = ProjectForm
    model = Project


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'todolistapp.delete_project'
    template_name = 'project/delete.html'
    model = Project
    success_url = reverse_lazy('todolistapp:project_index')
    form_class = ProjectDeleteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs


class ProjectChangeUser(PermissionRequiredMixin, UpdateView):
    permission_required = 'todolistapp.change_project_users'
    model = Project
    form_class = ProjectAddUserForm
    template_name = 'project/add-user.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectChangeUser, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all() \
            or self.request.user.is_superuser
