from django.db.models import Q
from django_filters import rest_framework as filters, OrderingFilter


from ..models import Payment
from ..constants import PaymentContentType


class PaymentFilter(filters.FilterSet):
    content_type = filters.CharFilter(label="Фильтр по типу продукта", method="content_type_filter")
    type = filters.CharFilter()

    order = OrderingFilter(fields=("date",), field_labels={"date": "Дата платежа"})

    class Meta:
        model = Payment
        fields = ()

    def content_type_filter(self, queryset, _: str, value):
        lookup = "content_type__model__icontains"

        match value:
            case PaymentContentType():
                q = Q(**{lookup: value.lower()})
            case _:
                q = Q()

        return queryset.filter(q)
