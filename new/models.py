from django.db import models
from account.models import Teacher
from django.utils.text import slugify

# Create your models here.


class New(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('account.Teacher', on_delete=models.CASCADE, null=True, blank=True, related_name='created_news')
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'new'
        verbose_name_plural = 'news'
