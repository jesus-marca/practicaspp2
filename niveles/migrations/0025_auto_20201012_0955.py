# Generated by Django 3.1.1 on 2020-10-12 04:25

import niveles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niveles', '0024_remove_lesson_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=niveles.models.save_lesson_files, verbose_name='Video'),
        ),
    ]
