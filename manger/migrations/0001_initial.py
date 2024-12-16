# Generated by Django 5.0.1 on 2024-09-01 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0015_remove_schoolclass_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='info_to_Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('Parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.parent', verbose_name='Parent')),
            ],
        ),
    ]
