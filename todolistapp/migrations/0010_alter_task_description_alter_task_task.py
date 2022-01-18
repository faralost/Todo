# Generated by Django 4.0 on 2022-01-18 15:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolistapp', '0009_alter_task_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=3000, null=True, validators=[django.core.validators.MaxLengthValidator(100)], verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task',
            field=models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Задача'),
        ),
    ]