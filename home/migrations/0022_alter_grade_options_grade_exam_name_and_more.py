# Generated by Django 5.0.1 on 2024-10-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_schedule_name_alter_schedule_end_time_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'verbose_name_plural': 'الدرجات'},
        ),
        migrations.AddField(
            model_name='grade',
            name='exam_name',
            field=models.CharField(default=1, max_length=100, verbose_name='اسم الامتحان'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='final_grade',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='الدرجة النهائية'),
            preserve_default=False,
        ),
    ]
