# Generated by Django 5.0.3 on 2024-04-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_remove_student_courses_course_students_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='enrolled_courses', to='account.student'),
        ),
    ]
