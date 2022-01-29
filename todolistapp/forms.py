from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from todolistapp.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['project']
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
    search = forms.CharField(max_length=100, required=False, label='поиск задач')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': widgets.Input(attrs={'size': 26}),
            'description': widgets.Textarea(attrs={'rows': 5, 'cols': 25}),
            'date_start': widgets.DateInput(attrs={'type': 'date'}),
            'date_end': widgets.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        if not date_end:
            return super(ProjectForm, self).clean()
        if date_end <= date_start:
            raise forms.ValidationError("Дата окончания должна быть позже даты начала!")
        return super(ProjectForm, self).clean()
