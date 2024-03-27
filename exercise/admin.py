from django.contrib import admin
from .models import Exercise


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "created_at", "deadline")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    search_fields = ("title", "body")


admin.site.register(Exercise, ExerciseAdmin)