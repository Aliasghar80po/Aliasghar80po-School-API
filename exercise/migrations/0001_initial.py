# Generated by Django 5.0.3 on 2024-03-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('attached_file', models.FileField(upload_to='exercise/exercise_files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
