from django.db import models


class Exercise(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    deadline = models.DateTimeField()
    attached_file = models.FileField(upload_to='exercise/exercise_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تمرین'
        verbose_name_plural = 'تمرینات'
