from django import forms
from django.forms import widgets

from todolistapp.models import Task


class TaskForm(forms.Form):
    task = forms.CharField(max_length=300, required=True, label="Задача:")
    status = forms.ChoiceField(required=True, label='Статус:', widget=widgets.Select,
                               choices=Task.status_choices)
    task_description = forms.CharField(max_length=3000, required=False, label='Описание:',
                                       widget=widgets.Textarea(attrs={'rows': 5, 'cols': 30}))
    deadline = forms.DateField(required=False, label='Дата выполнения:',
                               widget=widgets.DateInput(attrs={'placeholder': "ГГГГ-ММ-ДД", 'type': 'date'}))
