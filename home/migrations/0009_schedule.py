# Generated by Django 5.0.1 on 2024-08-10 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='وقت بدء الحصة')),
                ('end_time', models.TimeField(verbose_name='وقت انتهاء الحصة')),
                ('day_of_week', models.CharField(choices=[('Saturday', 'السبت'), ('Sunday', 'الأحد'), ('Monday', 'الاثنين'), ('Tuesday', 'الثلاثاء'), ('Wednesday', 'الأربعاء'), ('Thursday', 'الخميس'), ('Friday', 'الجمعة')], max_length=9, verbose_name='يوم الأسبوع')),
                ('school_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.schoolclass', verbose_name='الفصل')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject', verbose_name='المادة')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.teacher', verbose_name='اسم المدرس')),
            ],
            options={
                'verbose_name_plural': 'جداول الحصص',
            },
        ),
    ]
