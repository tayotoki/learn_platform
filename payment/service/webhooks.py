import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Payment
from .service_selector import stripe_service


@csrf_exempt
def stripe_webhook(request):
    """
    Описан специальный вэбхук для подтверждения платежей из сессии, для его настройки необходимо
    зарегистрировать его в Stripe dashboard, запросы на этот эндпоинт нужно отправлять через
    консольный клиент stripe. В дальнейшем можно создать celery-задачу по обновлению статусов.
    """

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_service.API_KEY
        )

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            Payment.objects.filter(**session.metadata).first().update(is_confirmed=True)

        return HttpResponse(status=200)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
