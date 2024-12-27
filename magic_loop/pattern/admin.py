from django.contrib import admin

from .models import Category, Pattern, Material, PatternTag, YarnType


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    list_editable = ("name",)
    list_per_page = 10


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "image",
        "file",
        "difficulty",
        "hook_or_needle_size",
        "saved_count",
    )
    list_filter = ("tag", "difficulty", "category")
    list_editable = ("difficulty",)
    sortable_by = ("saved_count",)
    search_fields = ("title", "description")
    list_per_page = 10


@admin.register(PatternTag)
class PatternTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_editable = ("name",)
    list_per_page = 10


@admin.register(YarnType)
class YarnTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_editable = ("name",)
    list_per_page = 10


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "pattern__id", "name", "amount", "unit")
    search_fields = ("name", "pattern__id")
    list_editable = ("name", "amount", "unit")
    list_per_page = 10
