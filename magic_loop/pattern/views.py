from django.core.cache import cache
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .tasks import send_pattern_saved_email

from .filtersets import PatternFilter, BasePatternFilter
from .models import Category, Pattern, PatternTag, Material, YarnType
from .serializers import (
    PatternTagSerializer,
    PatternSerializer,
    PatternDetailSerializer,
    AddPatternSerializer,
    DetailCategorySerializer,
    MaterialSerializer,
)
from utils.serializer_factory import SerializerFactory

SAVED_MILESTONE = 2


class PatternTagViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = PatternTag.objects.order_by("id")
    permission_classes = [IsAuthenticated]
    serializer_class = PatternTagSerializer


class YarnTypeViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = YarnType.objects.order_by("id")
    permission_classes = [IsAuthenticated]
    serializer_class = PatternTagSerializer


class PatternViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Pattern.objects.prefetch_related(
        "tag", "category", "materials", "yarn_type", "saved", "category__subcategories"
    ).select_related("author")
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerFactory(
        default=PatternSerializer,
        retrieve=PatternDetailSerializer,
        create=AddPatternSerializer,
    )

    filter_backends = [DjangoFilterBackend]
    filterset_class = PatternFilter

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == "saved_patterns":
            qs = qs.filter(saved=self.request.user)
            qs = qs.annotate(count_saved=Count("saved"))
            return qs

        return qs.annotate(count_saved=Count("saved")).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied("You can only delete your patterns.")
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        serializer_class=None,
        pagination_class=None,
        url_path="save",
        url_name="save",
    )
    def save_or_remove(self, request, pk=None):
        user = request.user
        pattern = self.get_object()
        if pattern:
            if request.method == "POST":
                user.saved_patterns.add(pattern)
                if pattern.saved_count % SAVED_MILESTONE == 0:
                    send_pattern_saved_email.delay(
                        pattern.title,
                        pattern.author.email,
                        pattern.author.username,
                        pattern.saved_count,
                    )
                return Response({"message": "Pattern saved successfully."})
            elif request.method == "DELETE":
                user.saved_patterns.remove(pattern)
                return Response({"message": "Pattern removed successfully."})

        return Response({"error": "Pattern not found."}, status=404)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        filterset_class=BasePatternFilter,
        url_path="saved-patterns",
        url_name="saved-patterns",
    )
    def saved_patterns(self, request):
        return super().list(request)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[],
        filterset_class=None,
        url_path="popular-patterns",
        url_name="popular-patterns",
    )
    def popular_patterns(self, request):
        cache_key = "popular_patterns"
        timeout = 60

        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        qs = self.get_queryset()
        qs = qs.order_by("-count_saved")[:15]

        serializer = self.get_serializer(qs, many=True)
        serialized_data = serializer.data

        cache.set(cache_key, serialized_data, timeout)

        return Response(serialized_data)


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.select_related("parent").prefetch_related(
        "subcategories"
    )
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerFactory(default=DetailCategorySerializer)


class MaterialViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Material.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MaterialSerializer
