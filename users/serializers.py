from rest_framework import serializers

from payment.serializers import PaymentListSerializer
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    payment_set = PaymentListSerializer(many=True)

    class Meta:
        model = User
        fields = ("email", "avatar", "city", "phone_number", "payment_set")


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
