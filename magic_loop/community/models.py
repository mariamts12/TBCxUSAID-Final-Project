from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tag = models.ManyToManyField(to=Tag, related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def comment_count(self) -> int:
        return self.comments.count()

    @property
    def has_pinned_answer(self) -> bool:
        return self.comments.filter(is_pinned=True).exists()

    def __str__(self):
        return f"{self.id}. {self.title}"


class PostImage(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='post_images/')


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    @property
    def likes(self):
        return self.feedback.filter(value=1).count()

    @property
    def dislikes(self):
        return self.feedback.filter(value=-1).count()

    def __str__(self):
        return f"{self.id}"


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, related_name="feedback", on_delete=models.CASCADE
    )
    value = models.IntegerField(choices=[(1, "Like"), (-1, "Dislike")])

    class Meta:
        unique_together = ("user", "comment")
