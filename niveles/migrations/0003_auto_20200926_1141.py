# Generated by Django 3.1.1 on 2020-09-26 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('niveles', '0002_auto_20200926_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='Standard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='niveles.standard'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='niveles.subject'),
        ),
    ]
