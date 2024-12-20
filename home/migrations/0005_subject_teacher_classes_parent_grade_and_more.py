# Generated by Django 4.2.4 on 2024-08-08 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_alter_attendance_date_alter_student_schoolclass_data_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='اسم المادة')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='classes',
            field=models.ManyToManyField(related_name='teachers', to='home.schoolclass', verbose_name='الفصول'),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('children', models.ManyToManyField(related_name='parents', to='home.student', verbose_name='الطلاب')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='اسم المستخدم')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='الدرجة')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='تاريخ إدخال الدرجة')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student', verbose_name='الطالب')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject', verbose_name='المادة')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(related_name='teachers', to='home.subject', verbose_name='المواد'),
        ),
    ]
