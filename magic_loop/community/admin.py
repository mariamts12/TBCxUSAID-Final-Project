from django.contrib import admin

from .models import Post, Comment, Tag, Feedback


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "content", "created_at")
    list_filter = ("tag", "author")
    search_fields = ("title", "content")
    list_editable = ("title",)
    list_per_page = 15


# @admin.register(PostImage)
# class PostImageAdmin(admin.ModelAdmin):
#     list_display = ("post", "image")
#     search_fields = ("post",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post__id",
        "content",
        "is_pinned",
        "likes",
        "dislikes",
        "created_at",
    )
    list_filter = ("author", "is_pinned")
    list_editable = ("is_pinned",)
    search_fields = ("post__id",)
    list_per_page = 15


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_editable = ("name",)
    list_per_page = 15


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment__id", "value")
    list_filter = ("user", "value")
    search_fields = ("comment__id",)
    list_editable = ("value",)
    list_per_page = 15
