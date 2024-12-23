from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, FeedbackViewSet, CommentViewSet, PostViewSet

app_name = "community"

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")
router.register("tags", TagViewSet, basename="tags")
router.register("comment", FeedbackViewSet, basename="feedback")
# router.register("post", LikePostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls), name="router"),
]
