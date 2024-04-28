# Generated by Django 5.0.3 on 2024-04-12 02:44

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[account.validators.national_code_validator], verbose_name='national code'),
        ),
    ]
