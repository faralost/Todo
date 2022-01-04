from django import forms
from django.forms import widgets


class TaskForm(forms.Form):
    task = forms.CharField(max_length=300, required=True, label="Задача")
    status = forms.CharField(max_length=20, required=True, label='Статус')
    task_description = forms.CharField(max_length=3000, required=False, label='Описание',
                                       widget=widgets.Textarea(attrs={'rows': 5, 'cols': 40}))
    deadline = forms.DateField(required=False, label='Дата выполнения')
