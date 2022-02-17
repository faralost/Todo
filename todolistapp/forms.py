from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import widgets

from todolistapp.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['project', 'is_deleted']
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
        exclude = ['users']
        widgets = {
            'name': widgets.Input(attrs={'size': 26}),
            'description': widgets.Textarea(attrs={'rows': 5, 'cols': 25}),
            'date_start': widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'date_end': widgets.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
        }

    def clean(self):
        try:
            date_start = self.cleaned_data['date_start']
            date_end = self.cleaned_data['date_end']
            if not date_end:
                return super(ProjectForm, self).clean()
            if date_end <= date_start:
                raise forms.ValidationError("Дата окончания должна быть позже даты начала!")
            return super(ProjectForm, self).clean()
        except KeyError:
            print("Введите правильную дату.")


class ProjectDeleteForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name",)

    def clean_name(self):
        if self.instance.name != self.cleaned_data.get("name"):
            raise ValidationError("Название введенного вами проекта не соответствует!")
        return self.cleaned_data.get("name")


class ProjectAddUserForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['users']
        widgets = {
            'users': widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kargs):
        self.user = kargs.pop('user')
        super().__init__(*args, **kargs)
        self.fields['users'].queryset = User.objects.filter(is_superuser=False)

    def clean(self):
        if not self.user.is_superuser and self.user not in self.cleaned_data.get('users'):
            raise ValidationError("Нельзя удалять себя из списка пользователей")
        return super(ProjectAddUserForm, self).clean()
