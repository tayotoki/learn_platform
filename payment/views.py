from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from .filters import PaymentFilter
from .models import Payment
from .serializers import PaymentListSerializer


@extend_schema(tags=["Payments"])
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related("content_type")
    serializer_class = PaymentListSerializer
    filterset_class = PaymentFilter
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminUser]
