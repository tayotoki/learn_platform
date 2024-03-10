from drf_spectacular.types import OpenApiTypes
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .constants import PaymentServicesType
from .filters import PaymentFilter
from .models import Payment
from .serializers import PaymentListSerializer, PaymentSerializer
from .service.service_selector import use_service


@extend_schema(tags=["Payments"])
class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Payment.objects.select_related("content_type")
    serializer_class = PaymentListSerializer
    filterset_class = PaymentFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == self.make_payment.__name__:
            serializer_class = PaymentSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["POST"])
    @use_service(service_name=PaymentServicesType.STRIPE)
    def make_payment(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return serializer.data

    @extend_schema(responses={status.HTTP_200_OK: OpenApiTypes.OBJECT},
                   examples=[
                       OpenApiExample(
                           "Примерный ответ",
                           value={"is_confirmed": True},
                           response_only=True
                       )
                   ])
    @action(detail=True, methods=["GET"])
    def get_payment_status(self, request, *args, **kwargs):
        """
        Получение статуса подтверждения платежа
        """
        payment = self.get_object()
        return Response({"is_confirmed": payment.is_confirmed}, status=status.HTTP_200_OK)
