# Generated by Django 5.0.1 on 2024-11-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint',
            options={'verbose_name': 'شكوى', 'verbose_name_plural': 'شكاوى'},
        ),
        migrations.RenameField(
            model_name='complaint',
            old_name='texst',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='Reviewed',
        ),
        migrations.AlterField(
            model_name='complaint',
            name='name',
            field=models.CharField(max_length=150, verbose_name='الاسم'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='reviewed',
            field=models.BooleanField(default=False, verbose_name='تم المراجعة'),
        ),
    ]
