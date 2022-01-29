from django.views.generic import ListView, DetailView

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
