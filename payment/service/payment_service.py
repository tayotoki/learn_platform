from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from courses.apps import CoursesConfig


class StripePaymentService:
    API_KEY = settings.STRIPE_API_KEY

    def __new__(cls, *args, **kwargs):
        stripe.api_key = cls.API_KEY
        return super().__new__(cls)

    def create_checkout_session(self, validated_data):
        content = (
            ContentType.objects
            .get(app_label=CoursesConfig.name, model=validated_data['content_type'])
            .model_class()
            .objects.get(pk=validated_data['object_id'])
        )
        amount = Decimal(validated_data['amount'])

        product = stripe.Product.create(
            name=content.name,
            type="service"
        )
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(amount * 100),
            currency="rub"
        )

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"http://0.0.0.0:8000/",
            metadata={
                **validated_data
            }
        )

        return session
