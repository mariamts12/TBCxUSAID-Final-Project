from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import DetailUserSerializer, UserSerializer, CreateUserSerializer
from utils.serializer_factory import SerializerFactory


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()

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
        permission_classes=[],
        serializer_class=CreateUserSerializer,
        url_path="sign_up",
        url_name="sign_up",
    )
    def sign_up(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
