from django import forms
from django.forms import widgets

from todolistapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'deadline': widgets.DateInput(attrs={'type': 'date'}),
            'task_description': widgets.Textarea(attrs={'rows': 5, 'cols': 30})
        }