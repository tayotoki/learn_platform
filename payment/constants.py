from django.db.models import TextChoices


class PaymentType(TextChoices):
    CASH = "cash", "наличные"
    NON_CASH = "non_cash", "безналичный"


class PaymentContentType(TextChoices):
    COURSE = "course", "курсы"
    LESSON = "lesson", "уроки"


class PaymentServicesType(TextChoices):
    STRIPE = "stripe", "страйп"
