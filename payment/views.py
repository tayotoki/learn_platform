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
from .service.service_selector import use_payment_service


@extend_schema(tags=["Payments"])
@use_payment_service(service_name=PaymentServicesType.STRIPE)
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

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
