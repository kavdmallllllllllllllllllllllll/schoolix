# Generated by Django 4.2.4 on 2024-08-08 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_alter_student_schoolclass_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='student',
            name='SchoolClass_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.schoolclass', verbose_name='الفصل'),
        ),
        migrations.AlterField(
            model_name='student',
            name='adres',
            field=models.TextField(verbose_name='عنوان السكن'),
        ),
        migrations.AlterField(
            model_name='student',
            name='ago',
            field=models.CharField(max_length=150, verbose_name='السن'),
        ),
        migrations.AlterField(
            model_name='student',
            name='father',
            field=models.CharField(max_length=150, verbose_name='اسم ولي الأمر'),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_nammber',
            field=models.CharField(max_length=150, verbose_name='رقم ولي الأمر'),
        ),
        migrations.AlterField(
            model_name='student',
            name='file_namber',
            field=models.CharField(max_length=150, verbose_name='رقم الملف'),
        ),
        migrations.AlterField(
            model_name='student',
            name='info',
            field=models.TextField(blank=True, null=True, verbose_name='ملحوظات عامة'),
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user/profile', verbose_name='صورة شخصية -')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='اسم المستخدم')),
            ],
        ),
    ]
