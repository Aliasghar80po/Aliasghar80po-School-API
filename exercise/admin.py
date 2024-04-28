from django.contrib import admin
from .models import Exercise, ExerciseResponse


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "created_at", "deadline")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    search_fields = ("title", "body")


admin.site.register(Exercise, ExerciseAdmin)


class ExerciseResponseAdmin(admin.ModelAdmin):
    list_display = ("exercise", "created_by", "response_date")


admin.site.register(ExerciseResponse, ExerciseResponseAdmin)
