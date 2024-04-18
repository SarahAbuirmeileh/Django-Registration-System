# Generated by Django 5.0.3 on 2024-04-08 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSchedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('days', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('room_number', models.CharField(max_length=20)),
            ],
        ),
    ]