# Generated by Django 5.0.1 on 2024-11-03 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_task_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='device_number',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='رقم الجهاز'),
        ),
    ]