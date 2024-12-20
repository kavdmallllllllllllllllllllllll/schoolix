# Generated by Django 5.0.1 on 2024-11-15 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_remove_leve_student_reason_absence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leve_student',
            name='permission_type',
            field=models.CharField(choices=[('بدون إذن', 'بدون إذن'), ('نصف يوم', 'نصف يوم'), ('إجازة بعذر', 'إجازة بعذر'), ('إجازة طبية', 'إجازة طبية'), ('حالة طارئة', 'حالة طارئة'), ('سبب آخر', 'سبب آخر')], default='none', max_length=50, verbose_name='نوع الإذن'),
        ),
    ]
