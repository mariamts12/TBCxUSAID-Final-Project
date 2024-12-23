from django.contrib import admin

from .models import Project, ProjectImage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "description",
        "pattern",
        "yarn_type",
        "hook_or_needle_size",
        "status",
        "start_date",
        "end_date",
        "time_spent"
    )
    list_filter = ("status", "pattern", "user")
    list_editable = ("status", "end_date", "time_spent")
    sortable_by = ("time_spent",)
    search_fields = ("name", "description", "pattern__name")
    list_per_page = 15


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "image")
    search_fields = ("project__name",)
    list_per_page = 15
