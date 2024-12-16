# Generated by Django 5.0.1 on 2024-08-24 02:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='academic_tasks',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='academic_tasks',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user/profile/Academic_tasks'),
        ),
    ]