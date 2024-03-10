"""Используем декоратор для быстрого переключения платежных сервисов во вьюхах"""


import functools
import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import StripePaymentService
from ..constants import PaymentServicesType
from ..serializers import PaymentSerializer

logger = logging.getLogger(__name__)

stripe_service = StripePaymentService()


# TODO: сделать подробную обработку ошибок от сервисов.
def use_service(service_name: str = None):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(view, *args, **kwargs):
            BAD_REQUEST = Response(status=status.HTTP_400_BAD_REQUEST)  # noqa

            match service_name:
                case PaymentServicesType.STRIPE:
                    try:
                        data = method(view, *args, **kwargs)
                        session = stripe_service.create_checkout_session(validated_data=data)
                        headers = view.get_success_headers(data)
                        return Response(
                                {
                                    "url": session.url,
                                    "session_id": session.id,
                                    "payment_intent": session.payment_intent,
                                    "metadata": session.metadata,
                                },
                                status=status.HTTP_201_CREATED,
                                headers=headers
                            )
                    except Exception as e:
                        logger.exception(e)
                        return BAD_REQUEST
                # Сюда добавляются остальные интегрированные сервисы для оплаты.
                case _:
                    return BAD_REQUEST
        return wrapper
    return decorator


def use_payment_service(service_name: str = None):
    def class_decorator(view_cls):
        class ServiceSelector(view_cls):
            def get_serializer_class(self):
                serializer_class = self.serializer_class

                if self.action == self.make_payment.__name__:
                    serializer_class = PaymentSerializer

                return serializer_class

            @use_service(service_name=service_name)
            @action(detail=False, methods=["POST"])
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

        return ServiceSelector
    return class_decorator
