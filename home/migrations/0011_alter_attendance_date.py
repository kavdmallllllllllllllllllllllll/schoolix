# Generated by Django 5.0.1 on 2024-08-12 02:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_schoolclass_options_schoolclass_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
