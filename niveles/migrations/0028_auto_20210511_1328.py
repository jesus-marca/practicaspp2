# Generated by Django 2.2.10 on 2021-05-11 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('niveles', '0027_timeslots_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslots',
            name='standard',
        ),
        migrations.RemoveField(
            model_name='timeslots',
            name='subject',
        ),
        migrations.CreateModel(
            name='SlotSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_subject', models.CharField(max_length=200)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard_slots_days', to='niveles.WorkingDays')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard_slots_time', to='niveles.TimeSlots')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='standard_slots', to='niveles.Standard')),
            ],
        ),
    ]
