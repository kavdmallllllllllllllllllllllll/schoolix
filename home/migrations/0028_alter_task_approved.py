# Generated by Django 5.0.1 on 2024-10-29 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_task_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='Approved',
            field=models.BooleanField(default=False),
        ),
    ]
