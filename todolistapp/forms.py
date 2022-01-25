from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from todolistapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'task': widgets.Input(attrs={'size': 26}),
            'description': widgets.Textarea(attrs={'rows': 5, 'cols': 25}),
            'types': widgets.CheckboxSelectMultiple()
        }
        error_messages = {
            'task': {'required': 'Это поле обязательное для заполнения!'},
            'status': {'required': 'Выберите один из статусов!'}

        }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='')
