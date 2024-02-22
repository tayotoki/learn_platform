from rest_framework import serializers

from payment.serializers import PaymentListSerializer
from users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор пользователя
    с полями без чувствительных данных
    """
    class Meta:
        model = User
        fields = ("email", "avatar", "city")


class UpdateUserSerializer(BaseUserSerializer):
    """
    Сериализатор пользователя для изменения/частичного изменения
    """
    class Meta:
        model = User
        exclude = (
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
        )


class UserProfileSerializer(BaseUserSerializer):
    """
    Сериализатор пользователя для получения полных данных
    """
    payment_set = PaymentListSerializer(many=True)

    class Meta:
        model = User
        fields = BaseUserSerializer.Meta.fields + ("phone_number", "payment_set")


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка пользователей
    """
    class Meta:
        model = User
        fields = ("id", "email")


class UserRegistrationSerializer(serializers.Serializer):
    """
    Сериализатор регистрации нового пользователя
    """
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'], password=validated_data['password1']
        )
        return user
