from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from ..constants import PaymentType
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа"""

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(app_label='courses'),
        slug_field='model'
    )
    object_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=PaymentType.choices, default=PaymentType.NON_CASH)

    class Meta:
        model = Payment
        fields = ['id', 'date', 'content_type', 'object_id', 'amount', 'type']
        extra_kwargs = {
            'date': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        payment = Payment.objects.create(user=user, **validated_data)
        return payment
