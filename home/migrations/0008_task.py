# Generated by Django 5.0.1 on 2024-08-09 07:48

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_attendance_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان المهمة')),
                ('description', ckeditor.fields.RichTextField(verbose_name='وصف المهمة')),
                ('due_date', models.DateField(verbose_name='تاريخ الاستحقاق')),
                ('is_completed', models.BooleanField(default=False, verbose_name='تمت المهمة')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.principal', verbose_name='تم التكليف بواسطة')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.teacher', verbose_name='تم التكليف إلى')),
            ],
            options={
                'verbose_name_plural': 'المهام',
            },
        ),
    ]
