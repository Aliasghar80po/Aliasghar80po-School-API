from django.contrib import admin
from .models import New


class NewAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "created_at", "last_modified")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    search_fields = ("title", "body")


admin.site.register(New, NewAdmin)