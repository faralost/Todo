from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Type(models.Model):
    name = models.CharField(max_length=30, verbose_name='Тип')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'types'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name='Статус')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    task = models.CharField(max_length=300, verbose_name='Задача', validators=(MinLengthValidator(5), RegexValidator(
        regex="^[a-zA-Zа-яА-Я ]+$",
        message="Название задачи должно состоять исключительно из букв!"
    )))
    description = models.TextField(max_length=3000, null=True, blank=True, default=None,
                                   verbose_name='Полное описание', validators=(MaxLengthValidator(500),))
    status = models.ForeignKey('todolistapp.Status', on_delete=models.PROTECT, related_name='tasks',
                               verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    types = models.ManyToManyField('todolistapp.Type', related_name='tasks', verbose_name='Типы')
    project = models.ForeignKey('todolistapp.Project', on_delete=models.CASCADE, related_name='tasks',
                                verbose_name='Проект')

    def get_absolute_url(self):
        return reverse('task_view', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.pk}. {self.task}"

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Project(models.Model):
    name = models.CharField(max_length=300, verbose_name='Название проекта', validators=(MinLengthValidator(5),))
    description = models.TextField(max_length=3000, verbose_name='Описание проекта',
                                   validators=(MaxLengthValidator(500),))
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания', null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
