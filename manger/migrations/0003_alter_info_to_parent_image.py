# Generated by Django 5.0.1 on 2024-09-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manger', '0002_info_to_parent_image_alter_info_to_parent_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_to_parent',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='info_to_Parent/'),
        ),
    ]
