from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_superuser')
    list_filter = ('is_superuser',)
    search_fields = ('username', 'email')
    list_editable = ("username",)
    list_per_page = 15
