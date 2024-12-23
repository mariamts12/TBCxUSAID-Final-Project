from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filtersets import PostFilter
from .models import Comment, Feedback, Post, Tag
from .serializers import (
    AddPostSerializer,
    PostSerializer,
    PostDetailSerializer,
    AddCommentSerializer,
    CommentSerializer,
    EvaluateCommentSerializer,
    FeedbackSerializer,
    TagSerializer,
)
from utils.serializer_factory import SerializerFactory


class TagViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Tag.objects.order_by("id")
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = (
        Post.objects.prefetch_related("tag", "comments", "likes")
        .select_related("author")
        .order_by("-created_at")
    )
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerFactory(
        default=PostSerializer,
        retrieve=PostDetailSerializer,
        create=AddPostSerializer,
    )

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied("You can only delete your posts.")
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        serializer_class=None,
        url_path="like",
        url_name="like",
    )
    def like_unlike(self, request, pk=None):
        user = request.user
        post = self.get_object()
        if post:
            if request.method == "POST":
                user.liked_posts.add(post)
                return Response({"message": "Post liked successfully."})
            elif request.method == "DELETE":
                user.liked_posts.remove(post)
                return Response({"message": "Post unliked successfully."})

        return Response({"error": "Post not found."}, status=404)


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.select_related("author").order_by(
        "-is_pinned", "-created_at"
    )
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerFactory(
        default=CommentSerializer, create=AddCommentSerializer
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def perform_update(serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied("You can only delete your comments.")
        return super().destroy(request, *args, **kwargs)

    def _evaluate(self, instance, action_name: str):
        context = {"action": action_name, "user": self.request.user}
        serializer = self.get_serializer(
            instance, data={}, partial=True, context=context
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {"id": instance.id, "action": action_name}
        return response_data

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=EvaluateCommentSerializer,
        url_path="pin",
        url_name="pin",
    )
    def pin(self, request, pk=None):
        instance = self.get_object()
        response_data = self._evaluate(instance, "pin")
        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=EvaluateCommentSerializer,
        url_path="unpin",
        url_name="unpin",
    )
    def unpin(self, request, pk=None):
        instance = self.get_object()
        response_data = self._evaluate(instance, "unpin")
        return Response(response_data, status=status.HTTP_200_OK)


class FeedbackViewSet(GenericViewSet):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def _create(self, data, action_name: str):
        context = {"action": action_name, "user": self.request.user}
        serializer = FeedbackSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.data

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="like",
        url_name="like",
    )
    def like(self, request):
        response_data = self._create(request.data, "like")
        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="dislike",
        url_name="dislike",
    )
    def dislike(self, request):
        response_data = self._create(request.data, "dislike")
        return Response(response_data, status=status.HTTP_201_CREATED)
