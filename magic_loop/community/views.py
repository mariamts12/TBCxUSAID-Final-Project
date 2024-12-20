from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filtersets import PostFilter
from .models import Comment, Feedback, Post, Tag, LikePost
from .serializers import (
    AddPostSerializer, PostSerializer, PostDetailSerializer,
    AddCommentSerializer, CommentSerializer, EvaluateCommentSerializer,
    FeedbackSerializer, TagSerializer, LikePostSerializer
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


class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.select_related("author").order_by("-is_pinned", "-created_at")
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


class LikePostViewSet(GenericViewSet):
    queryset = LikePost.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikePostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="like",
        url_name="like",
    )
    def like(self, request):
        serializer = LikePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if LikePost.objects.filter(post=serializer.validated_data["post"], user=request.user).exists():
            return Response({"message": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({"message": "Post liked successfully"}, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        url_path="unlike",
        url_name="unlike",
    )
    def unlike(self, request):
        serializer = LikePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = LikePost.objects.filter(post=serializer.validated_data["post"], user=request.user).first()

        if instance:
            instance.delete()
            return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)


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
