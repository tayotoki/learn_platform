from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from courses.serializers import CoursePaymentSerializer, LessonListSerializer
from ..constants import PaymentContentType
from ..models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка платежей
    """

    id = serializers.IntegerField(read_only=True)
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("id", "date", "amount", "content_type")
        read_only_fields = fields

    @extend_schema_field(field=CoursePaymentSerializer)
    def get_content_type(self, obj):
        content_type = ContentType.objects.get_for_model(obj.content_object)
        if content_type.model == PaymentContentType.COURSE:
            serializer = CoursePaymentSerializer(obj.content_object, many=False)
        elif content_type.model == PaymentContentType.LESSON:
            serializer = LessonListSerializer(obj.content_object, many=False)
        else:
            return None
        return serializer.data
