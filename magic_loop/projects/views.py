from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filtersets import ProjectFilter
from .models import Project
from .serializers import (
    ProjectSerializer,
    CreateProjectSerializer,
    ProjectDetailSerializer,
    UpdateProjectSerializer,
    ImageSerializer,
)
from utils.serializer_factory import SerializerFactory


class ProjectViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

    serializer_class = SerializerFactory(
        default=ProjectSerializer,
        retrieve=ProjectDetailSerializer,
        create=CreateProjectSerializer,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            raise PermissionDenied("You can only delete your own projects.")
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=UpdateProjectSerializer,
        url_name="update",
        url_path="update",
    )
    def update_project(self, request, pk=None):
        instance = self.get_object()

        if request.user != instance.user:
            return Response(
                {"detail": "You do not have permission to modify this project."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=ImageSerializer,
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_image(self, request, pk=None):
        project = self.get_object()

        if request.user != project.user:
            return Response(
                {
                    "detail": "You do not have permission to "
                    "upload images to this project."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
