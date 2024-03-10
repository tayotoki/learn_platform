"""Используем декоратор для быстрого переключения платежных сервисов во вьюхах"""


import functools
import logging

from rest_framework import status
from rest_framework.response import Response

from . import StripePaymentService
from ..constants import PaymentServicesType

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
