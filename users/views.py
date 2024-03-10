from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import (
    UserProfileSerializer,
    UserProfileListSerializer,
    UserRegistrationSerializer, BaseUserSerializer, UpdateUserSerializer
)
from .permissions import IsOwnerOrManager


@extend_schema(tags=["Profiles"])
class UserProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()

        if self.action == self.retrieve.__name__:
            queryset = queryset.prefetch_related("payment_set")
        return queryset

    def get_serializer_class(self):
        if self.action == self.retrieve.__name__:
            return (
                UserProfileSerializer
                if self.request.user == self.get_object()
                else BaseUserSerializer
            )
        if self.action == self.list.__name__:
            return UserProfileListSerializer
        if self.action in (self.update.__name__, self.partial_update.__name__):
            return UpdateUserSerializer

        return self.__class__.serializer_class

    @extend_schema(tags=["Profiles"], responses={status.HTTP_200_OK: UserProfileSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = self.permission_classes

        match self.action:
            case self.update.__name__ | self.partial_update.__name__ | self.destroy.__name__:
                permission_classes = [IsOwnerOrManager]

        return [permission() for permission in permission_classes]


@extend_schema(tags=["users"])
class RegisterViewSet(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
