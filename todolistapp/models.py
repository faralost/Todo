from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=30, verbose_name='Тип')

    class Meta:
        db_table = 'types'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    name = models.CharField(max_length=30, verbose_name='Статус')

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    task = models.CharField(max_length=300, verbose_name='Задача')
    description = models.TextField(max_length=3000, null=True, blank=True, default=None,
                                   verbose_name='Полное описание')
    status = models.ForeignKey('todolistapp.Status', on_delete=models.RESTRICT, related_name='tasks',
                               verbose_name='Статус')
    type = models.ForeignKey('todolistapp.Type', on_delete=models.RESTRICT, related_name='tasks', verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.pk}. {self.task}"

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
