from rest_framework import viewsets

from .filters import PaymentFilter
from .models import Payment
from .serializers import PaymentListSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related("content_type")
    serializer_class = PaymentListSerializer
    filterset_class = PaymentFilter
