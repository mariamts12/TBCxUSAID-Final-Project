from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import DetailUserSerializer, UserSerializer, CreateUserSerializer
from utils.serializer_factory import SerializerFactory


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.prefetch_related("saved_patterns", "patterns", "saved_patterns__tag",
                                             "patterns__tag", "projects", "posts")
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerFactory(
        default=UserSerializer,
        retrieve=DetailUserSerializer,
        create=CreateUserSerializer,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=CreateUserSerializer,
        url_path="sign-up",
        url_name="sign-up",
    )
    def sign_up(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
                    "message": "You have successfully registered!"
                },
            status=status.HTTP_201_CREATED
        )
