from django.db import models


class Task(models.Model):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'
    status_choices = [(new, 'Новая'), (in_progress, 'В процессе'), (done, 'Сделано')]

    task = models.CharField(max_length=300, verbose_name='Задача')
    status = models.CharField(max_length=20, choices=status_choices, default=new, verbose_name='статус')
    deadline = models.DateField(max_length=10, null=True, blank=True, default=None, verbose_name='Дата выполнения')
    task_description = models.TextField(max_length=3000, null=True, blank=True, default=None,
                                        verbose_name='Подробное описание')

    def __str__(self):
        return f"{self.pk}. {self.task}: {self.status}"

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
