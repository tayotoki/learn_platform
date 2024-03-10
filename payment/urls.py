from django.urls import path

from .apps import PaymentConfig
from .service.webhooks import stripe_webhook

app_name = PaymentConfig.name

urlpatterns = [
    path('stripe/webhook', stripe_webhook, name='stripe-webhook'),
]
