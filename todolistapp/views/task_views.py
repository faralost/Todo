from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from todolistapp.forms import TaskForm, SimpleSearchForm
from todolistapp.models import Task


class IndexView(ListView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(task__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by('-created_at')

    def post(self, request, *args, **kwargs):
        tasks_id = request.POST.getlist('tasks_id')
        for id in tasks_id:
            task = Task.objects.get(pk=id)
            task.delete()
        return redirect('index')

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


class TaskView(TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return super().get_context_data(**kwargs)


class TaskCreate(FormView):
    form_class = TaskForm
    template_name = 'task/task_create.html'

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})


class TaskDelete(View):
    def get(self, request, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        return render(request, 'task/delete.html', {'task': task})

    def post(self, request, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()
        return redirect('index')


class TaskUpdate(FormView):
    form_class = TaskForm
    template_name = 'task/update.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get("pk"))
