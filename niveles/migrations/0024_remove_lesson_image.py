# Generated by Django 3.1.1 on 2020-10-04 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niveles', '0023_auto_20201003_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='image',
        ),
    ]