# Generated by Django 5.0.1 on 2024-08-09 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_grade_options_alter_parent_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'verbose_name_plural': ' الغياب'},
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
    ]