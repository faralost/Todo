# Generated by Django 4.0 on 2022-01-15 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolistapp', '0004_alter_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='types',
            field=models.ManyToManyField(related_name='tasks', to='todolistapp.Type'),
        ),
    ]
