from django.utils import timezone
from datetime import timedelta
from django.db import models
from .validators import validate_zip_or_pdf


class Exercise(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    deadline = models.DateTimeField(default=timezone.now() + timedelta(days=4))
    attached_file = models.FileField(upload_to='exercise/exercise_files/', blank=True, null=True)
    created_by = models.ForeignKey('account.Teacher', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='created_exercise')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'


class ExerciseResponse(models.Model):
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name='responses')
    created_by = models.ForeignKey('account.Teacher', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='created_by_exercise')
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE)
    response_text = models.TextField()
    response_date = models.DateTimeField(auto_now_add=True)
    attached_file = models.FileField(upload_to='exercise/response_files/', validators=[validate_zip_or_pdf], blank=True,
                                     null=True)

    def __str__(self):
        return f"{self.student} - {self.exercise.title} Response"

    class Meta:
        verbose_name = 'Exercise Response'
        verbose_name_plural = 'Exercise Responses'
