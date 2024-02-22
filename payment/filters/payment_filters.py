from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django_filters import rest_framework as filters, OrderingFilter

from ..constants import PaymentContentType
from ..models import Payment


class PaymentFilter(filters.FilterSet):
    content_type = filters.CharFilter(
        label="Фильтр по типу продукта (course|lesson...)", method="content_type_filter"
    )
    type = filters.CharFilter()
    content_object_id = filters.NumberFilter(
        label="Фильтр по определенному продукту", method="content_object_filter"
    )
    order = OrderingFilter(fields=("date",), field_labels={"date": "Дата платежа"})

    class Meta:
        model = Payment
        fields = ()

    @staticmethod
    def content_type_filter(queryset, _: str, value):
        lookup = "content_type__model__icontains"

        match value:
            case PaymentContentType():
                q = Q(**{lookup: value.lower()})
            case _:
                q = Q()

        return queryset.filter(q)

    def content_object_filter(self, queryset, _: str, value):
        content_type = self.request.GET.get("content_type")
        if content_type:
            content_type = ContentType.objects.get(model=content_type.lower())
            queryset = queryset.filter(content_type=content_type, object_id=value)
        return queryset
