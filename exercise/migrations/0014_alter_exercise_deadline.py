# Generated by Django 5.0.3 on 2024-04-24 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0013_alter_exercise_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 28, 7, 33, 7, 749367, tzinfo=datetime.timezone.utc)),
        ),
    ]
