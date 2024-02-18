from rest_framework import viewsets

from payment.filters import PaymentFilter

from users.models import User
from users.serializers import UserProfileSerializer, UserProfileListSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        if self.action == self.retrieve.__name__:
            return User.objects.prefetch_related("payment_set")
        return self.__class__.queryset

    def get_serializer_class(self):
        if self.action == self.retrieve.__name__:
            return UserProfileSerializer
        if self.action == self.list.__name__:
            return UserProfileListSerializer
